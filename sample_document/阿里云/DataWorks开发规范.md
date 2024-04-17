# DataWorks开发规范指引文档

## 一、项目简述

​	为统计分析主流品牌的零辅食在不同电商平台的相关数据，特开发维护云听电商评论数据分析项目，其中原始数据来源于云听平台，数据接入方式为API接口接入，剩余的处理调度任务均通过DataWorks中的业务流程实现。首先将云听系统推送过来的原始数据(ods层)存入到阿里云rds数据库中，其次通过业务流程中的函数计算节点任务去触发函数fc中的代码处理逻辑将ods层数据进行初步处理成dwd层数据并存储到MaxCompute中，然后在业务流程中通过ODPS SQL节点任务将dwd层数据处理成dwm层，最后将处理好的dwm层数据通过业务流程中的离线同步节点将数据同步到rds中。以下操作步骤的实例中，ods层数据已提前在测试rds中准备好，python开发环境请使用Python 3.9。

## 二、操作步骤

### 步骤一：新建Github仓库

​	登录到github，新建一个名为'[dataworks_fc_demo](https://github.com/kyrie0704/dataworks_fc_demo)'的代码仓库。

### 步骤二：新建函数计算FC

​	登录到[函数计算控制台](https://fcnext.console.aliyun.com/cn-shenzhen/services)，创建服务及函数。

（1）创建服务

​	创建服务名称为'yunting_demo'的函数服务，并开启日志功能。

![创建服务](https://lf-development.oss-cn-shenzhen.aliyuncs.com/development_kyrie/dataworks_demo/%E5%88%9B%E5%BB%BA%E6%9C%8D%E5%8A%A1.png)

（2）创建函数

​	在'yunting_demo'服务中创建一个名为'yt_ods2dwd'的函数，请求处理程序类型选择【处理事件请求】，运行环境选择【Python 3.9】，代码上传方式选择【使用示例代码】，在高级配置中规格方案请配置为8核16GB，并将执行超时时间设置为36000秒，随后点击底部的【创建】按钮。

![](https://lf-development.oss-cn-shenzhen.aliyuncs.com/development_kyrie/dataworks_demo/%E5%88%9B%E5%BB%BA%E5%87%BD%E6%95%B0.png)

![](https://lf-development.oss-cn-shenzhen.aliyuncs.com/development_kyrie/dataworks_demo/%E5%88%9B%E5%BB%BA%E5%87%BD%E6%95%B02.png)

### 步骤三：新建云效流水线

​	登录到[云效平台](https://flow.aliyun.com/my?page=1)，创建流水线名称为''云听评论数据ods-dwd处理demo'流水线。配置流水线源为步骤一中创建的代码仓库的master分支，编辑函数计算应用发布为步骤二中创建的函数fc。

* 新建云效流水线；点击【新建流水线】，选择【其他】中的【其他 · 函数计算 (FC) 应用发布】并点击【创建】

![](https://lf-development.oss-cn-shenzhen.aliyuncs.com/development_kyrie/dataworks_demo/%E6%96%B0%E5%BB%BA%E6%B5%81%E6%B0%B4%E7%BA%BF.png)

![](https://lf-development.oss-cn-shenzhen.aliyuncs.com/development_kyrie/dataworks_demo/%E4%BA%91%E6%95%88%E5%88%9B%E5%BB%BA.png)

* 流水线源配置，选择代码源为【Github】，并选择步骤一中新建的代码仓库以及分支并点击【添加】。

![image-20231218151311408](https://lf-development.oss-cn-shenzhen.aliyuncs.com/development_kyrie/dataworks_demo/%E4%BA%91%E6%95%88%E6%B5%81%E6%B0%B4%E7%BA%BF%E6%BA%90.png)

* 函数计算(fc)应用发布配置，构建集群选择'云效中国香港构建集群'，指定构建节点选择'Linux/amd64'，下载流水线源选择'下载全部流水线源'，源码类型选择'本地代码'，代码路径填写'.'，如下图所示配置；点击右上角【仅保存】。

![image-20231218151311408](https://lf-development.oss-cn-shenzhen.aliyuncs.com/development_kyrie/dataworks_demo/%E4%BA%91%E6%95%88%E6%B5%81%E6%B0%B4%E7%BA%BFfc.png)

### 步骤四：新建业务流程

​	（1）登录到[DataWorks](https://dataworks.console.aliyun.com/overview)控制台，进入到[数据开发](https://ide2-cn-shenzhen.data.aliyun.com/)页面，新建业务名称为'yunting_demo'的业务流程。

![image-20231218155718769](https://lf-development.oss-cn-shenzhen.aliyuncs.com/development_kyrie/dataworks_demo/%E4%B8%9A%E5%8A%A1%E6%B5%81%E7%A8%8B.png)

​	（2）创建【begin】/【end】两个虚拟节点作为整个业务流程的开始/结束节点，虚拟节点为不产生任何数据的空跑节点。

![](https://lf-development.oss-cn-shenzhen.aliyuncs.com/development_kyrie/dataworks_demo/%E8%99%9A%E6%8B%9F%E8%8A%82%E7%82%B9.png)

### 步骤五：新建表

​	根据接口文档内容，创建并生成ods层的数据库表结构；分析ods层数据，为使数据变得更加规范和易用，从而创建dwd层的数据表，最后联系到最终需要输出的数据内容，进一步创建好dwm层的数据表。

(1)ods层表结构

准备一个mysql数据库用于存储ods层数据，生成以下结构的数据库表。

```sql
CREATE TABLE `yt_ec_review_test` (
  `id` int NOT NULL AUTO_INCREMENT,
  `analyzer` varchar(255) NOT NULL COMMENT 'NLP版本',
  `aspect` json DEFAULT NULL COMMENT '指标',
  `c_time` varchar(255) NOT NULL COMMENT '发布时间',
  `configs` json DEFAULT NULL COMMENT '系统主题配置',
  `connection_name` varchar(255) NOT NULL COMMENT '链接名称',
  `content` text NOT NULL COMMENT '评论内容',
  `data_level` varchar(255) NOT NULL COMMENT '数据类型，评论，追评等等(COMMENT：评论,COMMENT_APPEND：追评,COMMENT_REPLY：官方回复',
  `escore` varchar(255) NOT NULL COMMENT '通用情感，正面、中性、负面、混合',
  `group_id` varchar(255) NOT NULL COMMENT '原文，评论和回复所属的组的id',
  `oid` varchar(255) NOT NULL COMMENT '原始id',
  `parent` varchar(255) NOT NULL COMMENT '评论和回复的父原始id',
  `project_name` varchar(255) NOT NULL COMMENT '项目名称',
  `score` varchar(255) NOT NULL COMMENT '星级',
  `source_name` varchar(255) NOT NULL COMMENT '来源中⽂名：天猫等',
  `sku` varchar(255) NOT NULL COMMENT 'sku 两种格式(sku, spu;sku',
  `detail` varchar(255) NOT NULL COMMENT '销售属性',
  `title` varchar(255) NOT NULL COMMENT '标题',
  `u_name` varchar(255) NOT NULL COMMENT '评论作者名字',
  `unique_id` varchar(255) NOT NULL COMMENT '唯一id',
  `url` varchar(255) NOT NULL COMMENT '评论来源url，如果没有评论来源url则为为商品详情页面',
  `is_default` varchar(255) NOT NULL COMMENT '是否默认评论',
  `pictures` json DEFAULT NULL COMMENT '图片集合',
  `videos` json DEFAULT NULL COMMENT '视频集合',
  `is_plus` varchar(255) NOT NULL COMMENT 'plus会员标识（2022年9月27日增加）是/否',
  `multiple_group` varchar(255) NOT NULL COMMENT '多次拼单（2022年9月27日增加）',
  `created_at` varchar(255) NOT NULL COMMENT '初次入库时间，yyyy-MM-dd HH:mm:ss',
  `tag_name` json DEFAULT NULL COMMENT '标签名称 [''品牌效应'',''复购'''']',
  `insert_timestamp` varchar(255) NOT NULL COMMENT '具体发送数据的时间戳，精确到毫秒',
  `send_date` varchar(255) NOT NULL COMMENT '发送日期',
  `send_batch` varchar(255) NOT NULL COMMENT '当天传输的批次的最小时间',
  `count` varchar(255) NOT NULL COMMENT '当前批次传送的数量',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `modify_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `unique_id` (`unique_id`) USING BTREE,
  KEY `c_time` (`c_time`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='云听CEM-电商评论数据表-测试用';
```

(2)创建dwd层表

* 主表；在dataworks业务流程中，新建一个名为'create_dwd_yt_ec_review_main_test'的ODPS SQL节点，并输入以下内容。

```sql
--odps sql 
--********************************************************************--
--author:kyrie.lu
--create time:2023-11-28 10:14:07
--********************************************************************--
CREATE TABLE IF NOT EXISTS dwd_yt_ec_review_main_test(
	id INT COMMENT '主键id',
	analyzer STRING COMMENT 'NLP版本',
	c_time DATETIME COMMENT '发布时间',
	brand STRING COMMENT '品牌',
	category STRING COMMENT '品类',
	goods_id STRING COMMENT '商品ID',
	top_level STRING COMMENT '大类',
	store STRING COMMENT '店铺',
    platform STRING COMMENT '电商平台',
    platform_level STRING COMMENT '电商平台分类',
    connection_name STRING COMMENT '链接名称',
    content STRING COMMENT '评论内容',
    data_level STRING COMMENT '数据类型',
    escore STRING COMMENT '通用情感',
    group_id STRING COMMENT '原文，评论和回复所属的组的id',
    oid STRING COMMENT '原始id',
    parent STRING COMMENT '评论和回复的父原始id',
    project_name STRING COMMENT '项目名称',
	score STRING COMMENT '星级',
    source_name STRING COMMENT '来源中⽂名：天猫等',
    sku STRING COMMENT 'sku 两种格式(sku, spu;sku',
    detail STRING COMMENT '销售属性',
    title STRING COMMENT '标题',
	u_name STRING COMMENT '评论作者名字',
    uniques_id STRING COMMENT '唯一id',
    url STRING COMMENT '评论来源url，如果没有评论来源url则为为商品详情页面',
    is_default STRING COMMENT '是否默认评论',
    pictures JSON COMMENT '图片集合',
	videos JSON COMMENT '视频集合',
    is_plus STRING COMMENT 'plus会员标识（2022年9月27日增加）是/否',
    multiple_group STRING COMMENT '多次拼单（2022年9月27日增加）',
    created_at DATETIME COMMENT '初次入库时间，yyyy-MM-dd HH:mm:ss',
    tag_name JSON COMMENT '标签名称 [''品牌效应'',''复购'''']',
    send_date STRING COMMENT '发送日期',
	create_time DATETIME COMMENT '创建时间',
	modify_time DATETIME COMMENT '更新时间') 
STORED AS ALIORC  
TBLPROPERTIES("transactional"="true", 'comment'='云听CEM-电商评论数据主表');

```

![](https://lf-development.oss-cn-shenzhen.aliyuncs.com/development_kyrie/dataworks_demo/%E5%88%9B%E5%BB%BA%E8%A1%A8.png)

* 指标表；在dataworks业务流程中，新建一个名为'create_dwd_yt_ec_review_aspect_test'的ODPS SQL节点，并输入以下内容。

```sql
--odps sql 
--********************************************************************--
--author:kyrie.lu
--create time:2023-11-28 10:39:44
--********************************************************************--
CREATE TABLE IF NOT EXISTS dwd_yt_ec_review_aspect_test(
	id INT COMMENT '主键id',
    uniques_id STRING COMMENT '唯一id',
    escore STRING COMMENT '指标情感',
    aspect1 STRING COMMENT 'aspect1',
    aspect2 STRING COMMENT 'aspect2',
    send_date STRING COMMENT '发送日期',
	create_time DATETIME COMMENT '创建时间',
	modify_time DATETIME COMMENT '更新时间') 
STORED AS ALIORC  
TBLPROPERTIES("transactional"="true", 'comment'='云听CEM-电商评论数据指标表');
```

（3）创建dwm层表

* 云听评论统计-店铺品类维度；在dataworks业务流程中，新建一个名为'create_dwm_yunting_comment_tm'的ODPS SQL节点，并输入以下内容。

```sql
--odps sql 
--********************************************************************--
--author:edwin.wen
--create time:2023-12-06 11:09:23
--********************************************************************--

CREATE TABLE IF NOT EXISTS dwm_yunting_comment_tm_test(
	create_time DATETIME COMMENT '创建日期',
    update_time DATETIME COMMENT '更新日期',
	stat_time DATETIME COMMENT '统计日期',
    platform VARCHAR(255) COMMENT '平台',
    brand VARCHAR(255) COMMENT '品牌',
    store VARCHAR(255) COMMENT '店铺',
    category VARCHAR(255) COMMENT '品类',
    comment_tag_level1 VARCHAR(255) COMMENT '评论标签一级分类',
    comment_tag_level2 VARCHAR(255) COMMENT '评论标签二级分类',
    comment_tag_level3 VARCHAR(255) COMMENT '评论标签三级分类',
    complaint_type_level1 VARCHAR(255) COMMENT '客诉类型一级分类',
    complaint_type_level2 VARCHAR(255) COMMENT '客诉类型二级分类',
    complaint_type_level3 VARCHAR(255) COMMENT '客诉类型三级分类',
    complaint_type_dec VARCHAR(255) COMMENT '客诉类型中文描述',
    comment_cnt INT COMMENT '总评论数',
    positive_comment_cnt INT COMMENT '正面评论数',
    neutral_comment_cnt INT COMMENT '中性评论数',
    negative_comment_cnt INT COMMENT '负面评论数',
    valid_comment_cnt INT COMMENT '有效评论数',
    positive_valid_comment_cnt INT COMMENT '有效正面评论数',
    neutral_valid_comment_cnt INT COMMENT '有效中性评论数',
    negative_valid_comment_cnt INT COMMENT '有效负面评论数',
    comment_tag_cnt INT COMMENT '评论标签数',
    positive_comment_tag_cnt INT COMMENT '评论标签正面数',
    neutral_comment_tag_cnt INT COMMENT '评论标签中性数',
    negative_comment_tag_cnt INT COMMENT '评论标签负面数'
)
TBLPROPERTIES("transactional"="true", 'comment'='DWM云听评论统计-店铺品类维度');
```

### 步骤六：ODS层数据接入

将已提前准备好的1w条测试数据通过[点击链接](https://github.com/kyrie0704/dataworks_fc_demo/blob/master/yt_ec_review_test.sql)下载后导入到步骤五中新建的ods层的yt_ec_review_test表中。项目演示时可直接使用测试rds的kyrie库中yt_ec_review_test表作为ods层数据。

### 步骤七：ODS-DWD层处理

（1）本地编写业务代码 。

* index.py

```python
# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :  index.py
@Time    :  2023/10/19 17:12
@Author  :  Kyrie
@Email   :  Kyrie.Lu@littlefreddie.com
@Version :  1.0
@License :  (C)Copyright 2021-2022
@Desc    :  云听数据ods-dwd层处理
"""
import ast
import json
import warnings

import odps
import pandas as pd
from sqlalchemy import create_engine

warnings.filterwarnings("ignore")


class YtReviewInc:
    def __init__(self, access_id, secret_access_key, project, endpoint, yt_data_database_uri):
        # odps对象
        self.odps = odps.ODPS(access_id=access_id, secret_access_key=secret_access_key,
                              project=project, endpoint=endpoint)
        self.engine = create_engine(url=yt_data_database_uri)
        self.main_table = "dwd_yt_ec_review_main_test"
        self.aspect_table = "dwd_yt_ec_review_aspect_test"
        self.source_table_name = "yt_ec_review_test"

    def work(self):
        df = self.get_data_by_rds()
        if df.empty:
            print(f"没有新增/变更数据。。。")
            return
        # 重命名
        df.rename(columns={"unique_id": "uniques_id"}, inplace=True)
        # 提取配置信息中的品牌
        df["configs"] = df["configs"].apply(YtReviewInc.dispose_configs)
        df[["brand", "store", "platform", "category", "goods_id", "top_level", "platform_level"]] = \
            df["configs"].str.split("=", expand=True)
        aspect_df = df[["id", "aspect", "uniques_id", "create_time", "modify_time", "send_date"]]
        df.drop(columns=["aspect", "configs", "insert_timestamp", "send_batch"], inplace=True)
        # 删除MaxCompute已存在的记录
        self.delete_data(self.main_table, df["uniques_id"].tolist())
        # 主表数据入库
        self.save_main_by_odps(df)
        # 筛选值不为空的数据
        aspect_df = aspect_df[aspect_df["aspect"] != '[]']
        if not aspect_df.empty:
            # 将str转list
            aspect_df["aspect"] = aspect_df["aspect"].map(lambda x: json.loads(x))
            # 一列拆成多行
            aspect_df = aspect_df.explode("aspect")
            aspect_df["aspect"] = aspect_df["aspect"].apply(YtReviewInc.dispose_aspect)
            aspect_df[["escore", "aspect1", "aspect2"]] = aspect_df["aspect"].str.split("-", expand=True)
            aspect_df.drop(columns=["aspect"], inplace=True)
            # 删除MaxCompute已存在的记录
            self.delete_data(self.aspect_table, aspect_df["uniques_id"].tolist())
            # 指标数据入库
            self.save_aspect_by_odps(aspect_df)

    @staticmethod
    def dispose_aspect(json_data):
        """提取json数据中信息"""
        escore = json_data.get("escore")
        aspect1 = json_data.get("aspect1")
        aspect2 = json_data.get("aspect2")
        return escore + "-" + aspect1 + "-" + aspect2

    @staticmethod
    def dispose_configs(json_data):
        """提取json数据中信息"""
        li = ast.literal_eval(json_data)
        config_dict = {}
        for cate in li:
            config_dict.update(cate)
        brand = config_dict.get("品牌")
        store = config_dict.get("店铺")
        platform = config_dict.get("电商平台")
        category = config_dict.get("品类")
        goods_id = config_dict.get("商品ID")
        top_level = config_dict.get("大类")
        platform_level = config_dict.get("电商平台分类")
        values = brand + "=" + store + "=" + platform + "=" + category + "=" + goods_id + "=" + top_level + "=" + \
                 platform_level
        return values

    def get_data_by_rds(self):
        """获取rds数据库中原始表数据"""
        sql = f"SELECT * FROM {self.source_table_name} LIMIT 500"
        yt_df = pd.read_sql(sql, self.engine)
        return yt_df

    def delete_data(self, table_name, uniques_id_list):
        """根据uniques_id删除MaxCompute中存在的记录"""

        sql = f"DELETE FROM {table_name} WHERE uniques_id in {tuple(uniques_id_list)};"
        result = self.odps.execute_sql(sql)
        if not result:
            raise "删除主表数据异常"

    def save_main_by_odps(self, temp_df):
        """保存主表数据到MaxCompute"""
        temp_df = temp_df[["id", "analyzer", "c_time", "brand", "category", "goods_id", "top_level", "store",
                           "platform", "platform_level", "connection_name", "content", "data_level", "escore",
                           "group_id", "oid", "parent", "project_name", "score", "source_name", "sku", "detail",
                           "title", "u_name", "uniques_id", "url", "is_default", "pictures", "videos", "is_plus",
                           "multiple_group", "created_at", "tag_name", "send_date", "create_time", "modify_time"]]
        result = self.write_table(self.main_table, temp_df.values.tolist())
        if not result:
            print(f"主表数据入库失败")
            raise result

    def save_aspect_by_odps(self, temp_df):
        """保存指标数据到MaxCompute"""
        temp_df = temp_df[["id", "uniques_id", "escore", "aspect1", "aspect2", "send_date", "create_time",
                           "modify_time"]]
        result = self.write_table(self.aspect_table, temp_df.values.tolist())
        if not result:
            print(f"指标数据入库失败")
            raise result

    def write_table(self, table_name, record_list):
        """插入数据"""
        try:
            self.odps.write_table(table_name, record_list)
        except Exception as e:
            print(f"表 {table_name} 插入数据 {record_list} 失败； {e}")
            return False
        else:
            return True


def handler(event, context):
    evt = ast.literal_eval(event.decode())
    access_id_ = evt.get("access_id")
    secret_access_key_ = evt.get("secret_access_key")
    project_ = evt.get("project")
    endpoint_ = evt.get("endpoint")
    yt_data_database_uri_ = evt.get("yt_data_database_uri")
    YtReviewInc(access_id_, secret_access_key_, project_, endpoint_, yt_data_database_uri_).work()
    return 'ok'
```

* requirements.txt

```
odps==3.5.1
pandas==2.0.3
PyMySQL==1.1.0
SQLAlchemy==2.0.20
```

（2）将代码提交至[git仓库](https://github.com/kyrie0704/dataworks_fc_demo)。

（3）在[函数fc](https://fcnext.console.aliyun.com/overview)中配置python脚本运行所需的第三方依赖。

* 创建层

![](https://lf-development.oss-cn-shenzhen.aliyuncs.com/development_kyrie/dataworks_demo/%E5%88%9B%E5%BB%BA%E5%B1%82.png)

将本地requirements.txt中的内容复制到下图中的【requirements.txt文件】对应的输入框中。

![](https://lf-development.oss-cn-shenzhen.aliyuncs.com/development_kyrie/dataworks_demo/%E5%88%9B%E5%BB%BA%E4%BE%9D%E8%B5%96%E5%8C%85.png)

* 配置层

![](https://lf-development.oss-cn-shenzhen.aliyuncs.com/development_kyrie/dataworks_demo/%E9%85%8D%E7%BD%AE%E5%B1%82.png)

![](https://lf-development.oss-cn-shenzhen.aliyuncs.com/development_kyrie/dataworks_demo/%E9%85%8D%E7%BD%AE%E5%B1%822.png)

（4）点击运行步骤三中新建的[云效流水线](https://flow.aliyun.com/pipelines/2804475/current)，将git仓库中的代码同步至函数fc中。

![](https://lf-development.oss-cn-shenzhen.aliyuncs.com/development_kyrie/dataworks_demo/%E8%BF%90%E8%A1%8C%E4%BA%91%E6%95%88%E6%B5%81%E6%B0%B4%E7%BA%BF.png)

（5）在DataWorks的'yunting_demo'业务流程中创建[函数计算节点](https://ide2-cn-shenzhen.data.aliyun.com/?defaultProjectId=15760)，作为触发函数计算运行的节点。

* 新建函数计算节点

![image-20231218151443258](https://lf-development.oss-cn-shenzhen.aliyuncs.com/development_kyrie/dataworks_demo/dw%E5%88%9B%E5%BB%BAfc%E8%8A%82%E7%82%B9.png)

* 配置函数计算节点所需的变量信息，配置信息内容包括mysql数据库的连接信息和odps的连接信息。由于该变量属于敏感信息，故截屏做打码处理，此配置信息如有需要可向运维人员索取。

![](https://lf-development.oss-cn-shenzhen.aliyuncs.com/development_kyrie/dataworks_demo/%E8%B0%83%E7%94%A8fc%E8%8A%82%E7%82%B9.png)

### 步骤八：DWD-DWM层处理

​	在DataWorks的'yunting_demo'业务流程中创建名为'incremental_dwm_yunting_comment_tm'的ODPS SQL节点，编写如下的处理脚本。

```sql
--odps sql 
--********************************************************************--
--author:kyrie.lu
--create time:2024-01-03 14:14:07
--********************************************************************--
set odps.sql.hive.compatible=true;
INSERT INTO dwm_yunting_comment_tm_test(
    create_time
    ,update_time
    ,stat_time
    ,platform
    ,brand
    ,store
    ,category
    ,comment_tag_level1
    ,comment_tag_level2
    ,comment_tag_level3
    ,complaint_type_level1
    ,complaint_type_level2
    ,complaint_type_level3
    ,complaint_type_dec
    ,comment_cnt
    ,positive_comment_cnt
    ,neutral_comment_cnt
    ,negative_comment_cnt
    ,valid_comment_cnt
    ,positive_valid_comment_cnt
    ,neutral_valid_comment_cnt
    ,negative_valid_comment_cnt
    ,comment_tag_cnt
    ,positive_comment_tag_cnt
    ,neutral_comment_tag_cnt
    ,negative_comment_tag_cnt
)
SELECT
    cast(GETDATE() as datetime) as create_time,
    cast(GETDATE() as datetime) as update_time,
    cast(date_format(concat('${target_year_month}', '-01 00:00:00'),'yyyy-MM-dd 00:00:00') as datetime) as stat_time,
    cast (nvl(T.platform, '-1') as VARCHAR(255))
    ,cast (nvl(T.brand, '-1') as VARCHAR(255))
    ,cast (nvl(T.store, '-1') as VARCHAR(255))
    ,cast (nvl(T.category, '-1') as VARCHAR(255))
    ,cast (nvl(ct1.comment_tag_level1, '-1') as VARCHAR(255))
    ,cast (nvl(ct1.comment_tag_level2, '-1') as VARCHAR(255))
    ,cast (nvl(T.aspect2, '-1') as VARCHAR(255)) as comment_tag_level3
    ,cast (nvl(ct2.complaint_type_level1, '-1') as VARCHAR(255))
    ,cast (nvl(ct2.complaint_type_level2, '-1') as VARCHAR(255))
    ,cast (nvl(ct2.complaint_type_level3, '-1') as VARCHAR(255))
    ,cast (nvl(ct2.complaint_type_desc_cn, '-1') as VARCHAR(255))
    ,cast (nvl(T.comment_cnt, 0) as INT)
    ,cast (nvl(T.positive_comment_cnt, 0) as INT)
    ,cast (nvl(T.neutral_comment_cnt, 0) as INT)
    ,cast (nvl(T.negative_comment_cnt, 0) as INT)
    ,cast (nvl(T.valid_comment_cnt, 0) as INT)
    ,cast (nvl(T.positive_valid_comment_cnt, 0) as INT)
    ,cast (nvl(T.neutral_valid_comment_cnt, 0) as INT)
    ,cast (nvl(T.negative_valid_comment_cnt, 0) as INT)
    ,cast (nvl(T.comment_tag_cnt, 0) as INT)
    ,cast (nvl(T.positive_comment_tag_cnt, 0) as INT)
    ,cast (nvl(T.neutral_comment_tag_cnt, 0) as INT)
    ,cast (nvl(T.negative_comment_tag_cnt, 0) as INT)
FROM (
    SELECT
        platform
        ,brand
        ,store
        ,category
        ,aspect2
        ,count(distinct t1.uniques_id) as comment_cnt
        ,count(distinct(IF(t1.escore = '正面', t1.uniques_id, null))) as positive_comment_cnt
        ,count(distinct(IF(t1.escore = '中性', t1.uniques_id, null))) as neutral_comment_cnt
        ,count(distinct(IF(t1.escore = '负面', t1.uniques_id, null))) as negative_comment_cnt
        ,count(distinct(IF(t1.is_default != '是', t1.uniques_id, null))) as valid_comment_cnt
        ,count(distinct(IF(t1.is_default != '是' and t1.escore = '正面', t1.uniques_id, null))) as positive_valid_comment_cnt
        ,count(distinct(IF(t1.is_default != '是' and t1.escore = '中性', t1.uniques_id, null))) as neutral_valid_comment_cnt
        ,count(distinct(IF(t1.is_default != '是' and t1.escore = '负面', t1.uniques_id, null))) as negative_valid_comment_cnt
        ,count(1) as comment_tag_cnt
        ,sum(IF(t1.is_default != '是' and t2.escore = '正面', 1, 0)) as positive_comment_tag_cnt
        ,sum(IF(t1.is_default != '是' and t2.escore = '中性', 1, 0)) as neutral_comment_tag_cnt
        ,sum(IF(t1.is_default != '是' and t2.escore = '负面', 1, 0)) as negative_comment_tag_cnt
    FROM(
        SELECT
            uniques_id,
            platform,
            brand,
            store,
            category,
            is_default,
            escore
        FROM dwd_yt_ec_review_main_test
    ) t1
    LEFT JOIN (
        SELECT
            uniques_id,
            escore,
            aspect1,
            aspect2
        FROM dwd_yt_ec_review_aspect_test
    ) t2 on t1.uniques_id = t2.uniques_id
    WHERE 1=1
    GROUP BY platform, brand, store, category, aspect2
) T
LEFT JOIN scm_yunting_comment_tag ct1 
    on T.aspect2 = ct1.comment_tag_level3 
    and cast(ct1.end_date as date) = '9999-12-31'
    -- and cast(ct1.start_date as date) <= '${target_date}'
    -- and cast(ct1.end_date as date) > '${target_date}'
LEFT JOIN scm_yunting_complaint_type ct2 
    on ct1.comment_tag_level3 = ct2.comment_tag_level3
    and cast(ct2.end_date as date) = '9999-12-31'
    -- and cast(ct2.start_date as date) <= '${target_date}'
    -- and cast(ct2.end_date as date) > '${target_date}'
WHERE 1=1
;
```

### 步骤九：提交流程节点

（1）将所有节点按执行顺序进行连线，连好线后单击右上角的格式化图标，如下图。

![](https://lf-development.oss-cn-shenzhen.aliyuncs.com/development_kyrie/dataworks_demo/%E6%B5%81%E7%A8%8B%E8%BF%9E%E7%BA%BF.png)

（2）批量配置业务流程的调度资源组。

* 右键业务流程，选择【批量操作】

![image-20231218162805083](https://lf-development.oss-cn-shenzhen.aliyuncs.com/development_kyrie/dataworks_demo/%E6%89%B9%E9%87%8F%E6%93%8D%E4%BD%9C1.png)

* 选中所有的节点，在底部导航栏中点击【更多】-【修改调度资源组】

![](https://lf-development.oss-cn-shenzhen.aliyuncs.com/development_kyrie/dataworks_demo/%E6%89%B9%E9%87%8F%E6%93%8D%E4%BD%9C2.png)

* 选择资源组为"lf_offline_project"，选中"知悉风险并确认操作"，最后点击【确认】

![](https://lf-development.oss-cn-shenzhen.aliyuncs.com/development_kyrie/dataworks_demo/%E6%89%B9%E9%87%8F%E6%93%8D%E4%BD%9C3.png)

（2）点击【运行】测试完整流程。

![image-20231218162938435](https://lf-development.oss-cn-shenzhen.aliyuncs.com/development_kyrie/markdown%E6%96%87%E4%BB%B6%E6%88%AA%E5%B1%8F/typora-user-images/image-20231218162938435.png)

（3）点击【提交】，将节点提交至开发环境。

![image-20231218163117752](https://lf-development.oss-cn-shenzhen.aliyuncs.com/development_kyrie/markdown%E6%96%87%E4%BB%B6%E6%88%AA%E5%B1%8F/typora-user-images/image-20231218163117752.png)

## 三、常见问题

1、函数计算FC默认以UTC时间运行。

​	函数计算默认以UTC时间运行，也就是0时区，即北京时间减去8个小时。例如北京时间每天12:00，转化为UTC时间就是每天04:00。可以通过设置环境变量进行时区修改，例如，设置变量**TZ**的值为`Asia/Shanghai`后，函数计算的时区被修改为东8区，即北京时间。

2、云效流水线的集群构建默认使用北京构建集群。

​	云效流水线中，在任务节点选择构建集群，默认使用**云效北京构建集群**。在此配置下，下载或者连接海外服务的时候，会出现失败或者速度过慢的现象。可通过将集群配置为**云效香港构建集群**来解决下载海外构建依赖或者连接海外服务的场景需求。

3、权限问题

​	如遇到某个服务没有相关的操作权限，请联系运维人员。

## 四、附件

[云听项目设计](https://doc.weixin.qq.com/sheet/e3_AYQA4Aa4AIsYQXKoviyTxepwKOri7?scode=ANwALQc9AA0sI0gvvAAYQA4Aa4AIs&tab=qcm715)

​	