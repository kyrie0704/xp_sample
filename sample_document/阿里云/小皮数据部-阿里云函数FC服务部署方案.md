# 小皮数据部-阿里云函数FC服务部署方案

### 一、简介

#### 1、函数FC

* 函数计算是事件驱动的全托管计算服务。使用函数计算，您无需采购与管理服务器等基础设施，只需编写并上传代码。函数计算为您准备好计算资源，弹性地、可靠地运行任务，并提供日志查询、性能监控和报警等功能

> 帮助文档：https://help.aliyun.com/product/50980.html

#### 2、云效流水线

* 流水线又名「Flow」，是一款企业级、自动化的研发交付流水线， 提供灵活易用的持续集成、持续验证、 持续发布功能，帮助企业高质量、高效率的交付业务
* 流水线是持续交付的载体，通过构建自动化、集成自动化、验证自动化、部署自动化，完成从开发到上线过程的持续交付

> 帮助文档：https://help.aliyun.com/document_detail/153116.html

#### 3、云监控

* 一项针对阿里云资源和互联网应用进行监控的服务。

> 帮助文档：https://www.alibabacloud.com/help/zh/cloudmonitor/latest/what-is-cloudmonitor

### 二、部署方案

#### 1、代码提交

本地开发完成后，将代码提交至git仓库

#### 2、创建fc 服务及函数

**创建服务操作步骤**

1、登录[函数计算控制台](https://fcnext.console.aliyun.com/overview)

2、在左侧导航栏，单击 **服务及函数**

3、在顶部菜单栏，选择 **地域**

4、在 **服务列表**，单击 **创建服务**；填写服务名称和描述，选择启用日志功能，单击 **确定**

**创建函数操作步骤**

1、点击进入创建的服务

2、在 **函数管理** 页面，单击 **创建函数**

3、在 **创建函数** 页面，选择 `使用标准 Runtime 从零创建`

4、在基本设置区域，完成相关参数的设置后，单击 **创建**

* 函数名称：设置函数名称
* 运行环境：选择python3.6/python3.9
* 代码上传方式：使用示例代码
* 请求处理程序类型：非web服务统一选择 处理事件请求
* 实例类型：按项目需要选择 弹性实例/性能实例
* 实例并发度：设置为1 (可根据具体需求增加并发度)
* 请求处理程序：设置为index.handler(可根据具体需求更换)

5、在**函数配置**区域，完成相关参数设置

* 基础信息：设置内存规格
* 基础信息：设置实例并发度
* 环境信息：设置执行超时时间
* 环境变量：设置环境变量    `{'DEBUG': true/false}`
* 层：配置服务依赖的层(第三方库)

6、在**触发器管理**区域，设置触发器

* 创建触发器：选择对应的(定时/其他)触发器类型并创建

`环境变量配置`: 函数计算FC -> 服务及函数 -> 选择对应服务 -> 选择对应函数 -> 函数配置 -> 环境信息

*注意：*

> * 如果python开发需要安装第三方依赖库，请在函数计算最外层目录下选择 层管理 --> 创建层，完成相应模块的安装
> * 可通过环境变量配置一些公共参数
> * 可通过NAS文件系统挂载方式处理文件的创建和写入(eg:运行日志的记录)
> * 如果函数运行时长较长，需要将 函数配置->环境信息->执行超时时间(默认60秒) 设置的长一点；但最长不超过24小时

#### 3、创建流水线

1、登录[云效控制台](https://devops.console.aliyun.com/organizations)，选择流水线 Flow，进入工作

2、在 **流水线 Flow** 右上角，单击 **新建流水线**

3、在 **选择流水线模板弹窗**中，选择 **其他** -> **其他*函数计算(FC)应用发布**，单击 **创建**

4、在**流程配置**页面，选择**添加流水线源**

* 代码源：选择代码源 -> Github
  * 服务连接：选择或添加服务链接
  * 仓库：选择项目仓库
  * 默认分支：选择master分支
  * 开启代码源触发：开启并在GitHub配置该Webhook

5、点击 **函数计算(fc)应用发布**，**编辑** -> **任务步骤** -> **阿里函数计算部署** 将代码部署到对应的fc

* 源码类型：选择 `本地代码`
* 代码路径：填写 `.`
* 任务插件：用作流水线运行(成功/失败/取消/跳过/等待执行)状态的(邮箱/企业微信等)通知，可根据需要选择配置

6、单击保存并运行

*注意：*

> * 如果代码仓库为github，首次选择代码源时，需要添加服务连接，步骤为：添加服务连接 --> 新建 -->  选择 使用范围 --> 点击 创建
> * 编辑 阿里云函数计算部署时，源码类型请选择 `本地代码`，代码路径请填写 `.`

### 三、监控告警

#### 1、设置告警联系人

1、登录[云监控](https://cloudmonitornext.console.aliyun.com/alert-contactGroup)，左侧导航栏选择 **报警服务** -> **报警联系人**

2、点击 **新建联系人**，设置报警联系人信息

3、选择 **报警联系组**，点击 **新建联系组**，选择联系人，完成联系组的添加

#### 2、创建告警规则

1、左侧导航栏选择 **报警服务** -> **报警规则**

2、点击 **创建报警规则** 

* 产品：选择 `函数计算`
* 资源范围：通用告警选择 `全部资源`，针对性告警选择 `实例`
* **添加规则**：完成规则添加
* 通道沉默周期：默认为24小时 
* 生效时间：00:00 - 23:59
* 报警联系人组：选择需要推送报警信息的联系人组

> [通道沉默周期](https://www.alibabacloud.com/help/zh/cloudmonitor/latest/terms)： 报警发送后，如果该监控项在通道沉默周期之内持续超过报警阈值，则在通道沉默周期内不会再次触发报警。

