# -*- coding: utf-8 -*-
# @Author: Kyrie
# @Email: Kyrie.Lu@littlefreddie.com
# @Time: 2022/7/21 16:32
# @Desc: 配置信息
import os
import sys


sys.path.append(os.path.dirname(os.path.realpath(__file__)))
try:
    debug = os.environ.get("DEBUG")
    if str(debug).lower() == 'false':
        debug = False
    else:
        debug = True
except KeyError:
    debug = True


class Config:
    """公共配置项"""
    # 日志存放路径
    log_dir = os.path.join('/tmp', "logs")
    # 日志文件名
    log_name = "bank.log"

    # 高德地图api配置信息
    app_code = '***'


class ProductConfig(Config):
    """正式环境"""
    # mysql
    database_uri = "mysql+pymysql://user:passwd@ip:port/database"
    # 数据库连接池大小
    pool_size = 30
    # 连接池回收时间
    pool_recycle = 3600


class TestConfig(Config):
    """测试环境"""
    # mysql
    database_uri = "mysql+pymysql://user:passwd@ip:port/database"
    # 数据库连接池大小
    pool_size = 30
    # 连接池回收时间
    pool_recycle = 3600
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:test123@127.0.0.1:3307/test_db?charset=utf8mb4"


if debug:
    config = TestConfig()
else:
    config = ProductConfig()
