# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :  sys_info_api.py
@Time    :  2023/2/6 15:19
@Author  :  Kyrie
@Email   :  Kyrie.Lu@littlefreddie.com
@Version :  1.0
@License :  (C)Copyright 2021-2022
@Desc    :  系统信息管理
"""
import ast
import uuid
import datetime

import requests
from api.waiqin import WaiQin


class SystemInfo(WaiQin):
    def query_area_code(self):
        """
        查询行政区划基本信息
        https://api.waiqin365.com/SERVER/sysapp/dictionary.html
        """
        body = {}
        msg_id = uuid.uuid4()
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        digest = self.cal_sign(body, timestamp)
        api = "api/dictionary/v1/queryAreaCode"
        url = f"{self.host}/{api}/{self.openid}/{timestamp}/{digest}/{str(msg_id)}"
        try:
            response = requests.post(url=url, json=body)
            json_data = response.json()
        except Exception as e:
            print(f"查询行政区划基本信息接口调用异常，error:{e}")
            return None
        if json_data.get("return_code") == "0":
            return ast.literal_eval(json_data.get("response_data"))
        else:
            print(f"查询行政区划基本信息接口返回错误，错误信息：{json_data.get('return_msg')}")
            return None


if __name__ == "__main__":
    data = SystemInfo().query_area_code()
    print(data)
