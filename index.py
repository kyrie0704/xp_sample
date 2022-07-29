# -*- coding: utf-8 -*-
# @Author: Kyrie
# @Email: Kyrie.Lu@littlefreddie.com
# @Time: 2022/7/21 16:28
# @Desc: 函数FC执行入口
import logging


def handler(event, context):
    """
    函数FC入口
    :param event: 调用函数时传入的参数
    :param context: 提供在调用时的运行上下文信息。
    """
    # 打印和查看日志 https://help.aliyun.com/document_detail/422184.html
    logger = logging.getLogger()
    logger.info("test")
    return "hello world"
