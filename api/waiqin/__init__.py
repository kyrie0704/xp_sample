# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :  __init__.py.py
@Time    :  2023/1/31 15:23
@Author  :  Kyrie
@Email   :  Kyrie.Lu@littlefreddie.com
@Version :  1.0
@License :  (C)Copyright 2021-2022
@Desc    :  勤策 API开发平台
"""
import json
from hashlib import md5


class WaiQin:
    def __init__(self, openid, appkey):
        self.host = 'https://sfa.littlefreddie.cn'
        self.openid = openid
        self.appkey = appkey

    def cal_sign(self, body, timestamp):
        """
        计算签名
        :parma body: json格式消息体
        :parma timestamp: 请求消息时间。格式：yyyyMMddHHmmSS
        """
        en = (str(json.dumps(body)) + "|" + str(self.appkey) + "|" + str(timestamp)).encode('utf-8')
        return md5(en).hexdigest()
