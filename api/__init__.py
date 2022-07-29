# -*- coding: utf-8 -*-

import fc2

client = fc2.Client(
    endpoint='<Your Endpoint>',
    accessKeyID='<Your AccessKeyID>',
    accessKeySecret='<Your AccessKeySecret>')

service_name = "bank_data"
function_name = "function_name"
trigger_name = "trigger_name"

# 创建服务。
client.create_service(service_name)

# 创建服务时配置VPC信息。
vpcConfig = {
        'vpcId': '<Your Vpc Id>',
        'vSwitchIds': '<[Your VSwitch Ids]>',
        'securityGroupId': '<Your Security Group Id>'
}

# 创建服务时创建vpcConfig。
# 当需要设置VPC配置时，需设置角色。
vpc_role = 'acs:ram::12345678:role/aliyunvpcrole'

# 创建服务时设置NAS配置。
nasConfig = {
       "userId": '<The NAS file system user id>',
       "groupId": '<The NAS file system group id>',
       "mountPoints": [
            {
                "serverAddrserverAddr": '<The NAS file system mount target>',
                "mountDir": '<The mount dir to the local file system>',
            }
       ],
}

service = client.create_service(service_name, role=vpc_role, vpcConfig=vpcConfig, nasConfig=nasConfig)

# 创建函数。
# 当前目录有一个main.zip文件（main.py有一个myhandler函数）。
# 设置环境变量{'testKey': 'testValue'}。
client.create_function(service_name, function_name, 'python3',  'main.my_handler', codeZipFile='main.zip',
                       environmentVariables={'testKey': 'testValue'})

# 创建Initializer函数。
# main.my_initializer是初始化界面的入口点。
client.create_function(service_name, function_name, 'python3',  'main.my_handler', "main.my_initializer",
                       codeZipFile='main.zip', environmentVariables={'testKey': 'testValue'})

# 同步调用函数。
client.invoke_function(service_name, function_name)

# 创建触发器。
# 创建OSS触发器。
oss_trigger_config = {
        'events': ['oss:ObjectCreated:*'],
        'filter': {
            'key': {
                'prefix': 'prefix',
                'suffix': 'suffix'
            }
        }
}
source_arn = 'acs:oss:cn-shanghai:12345678:bucketName'
invocation_role = 'acs:ram::12345678:role/aliyunosseventnotificationrole'
client.create_trigger(service_name, function_name, trigger_name, 'oss', oss_trigger_config, source_arn,
                      invocation_role)

# 创建日志服务触发器。
log_trigger_config = {
        'sourceConfig': {
            'logstore': 'log_store_source'
        },
        'jobConfig': {
            'triggerInterval': 60,
            'maxRetryTime': 10
        },
        'functionParameter': {},
        'logConfig': {
            'project': 'log_project',
            'logstore': 'log_store'
        },
        'enable': False
}
source_arn = 'acs:log:cn-shanghai:12345678:project/log_project'
invocation_role = 'acs:ram::12345678:role/aliyunlogetlrole'
client.create_trigger(service_name, function_name, trigger_name, 'oss', log_trigger_config, source_arn,
                      invocation_role)
# 创建定时触发器。
time_trigger_config = {
        'payload': 'awesome-fc',
        'cronExpression': '0 5 * * * *',
        'enable': True
}
client.create_trigger(service_name, function_name, trigger_name, 'timer', time_trigger_config, '', '')

# 调用带有输入参数的函数。
client.invoke_function(service_name, function_name, payload=bytes('hello_world'))

# 读取图像并以文件数据作为输入参数调用函数。
src = open('src_image_file_path', 'rb')  # Note: please open it as binary.
r = client.invoke_function(service_name, function_name, payload=src)

# 将结果保存为输出图像。
dst = open('dst_image_file_path', 'wb')
dst.write(r.data)
src.close()
dst.close()

# 异步调用函数。
client.invoke_function(service_name, function_name, headers={'x-fc-invocation-type': 'Async'})

# 获取服务列表。
client.list_services()

# 获取带有前缀和限制的函数列表。
client.list_functions(service_name, prefix='the_prefix', limit=10)

# 删除服务。
client.delete_service(service_name)

# 删除函数。
client.delete_function(service_name, function_name)
