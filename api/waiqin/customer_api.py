# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :  customer_api.py
@Time    :  2023/2/1 15:45
@Author  :  Kyrie
@Email   :  Kyrie.Lu@littlefreddie.com
@Version :  1.0
@License :  (C)Copyright 2021-2022
@Desc    :  客户管理
"""
import ast
import uuid
import datetime

import requests
from api.waiqin import WaiQin


class Customer(WaiQin):
    def query_customer(self, page, params=None):
        """
        查询经销商
        :param page: 页码
        :param params: 请求参数
        """
        body = {
            "page_number": str(page)
        }
        if params:
            body.update(params)
        msg_id = uuid.uuid4()
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        digest = self.cal_sign(body, timestamp)
        api = "api/dealer/v1/queryDealer"
        url = f"{self.host}/{api}/{self.openid}/{timestamp}/{digest}/{str(msg_id)}"
        try:
            response = requests.post(url=url, json=body)
            json_data = response.json()
        except Exception as e:
            print(f"查询经销商接口调用异常，error:{e}")
            return None
        if json_data.get("return_code") == "0":
            return ast.literal_eval(json_data.get("response_data"))
        else:
            print(f"查询经销商接口返回错误，错误信息：{json_data.get('return_msg')}")
            return None

    def query_district(self, dis_id=None):
        """
        查询销售区域
        :param dis_id: 销售区域唯一标识(source_code)
        """
        body = {}
        if dis_id:
            body.update({"dis_id": dis_id})
        msg_id = uuid.uuid4()
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        digest = self.cal_sign(body, timestamp)
        api = "api/district/v1/queryDistrict"
        url = f"{self.host}/{api}/{self.openid}/{timestamp}/{digest}/{str(msg_id)}"
        try:
            response = requests.post(url=url, json=body)
            json_data = response.json()
        except Exception as e:
            print(f"查询销售区域接口调用异常，error:{e}")
            return None
        if json_data.get("return_code") == "0":
            return ast.literal_eval(json_data.get("response_data"))
        else:
            print(f"查询销售区域接口返回错误，错误信息：{json_data.get('return_msg')}")
            return None


if __name__ == "__main__":
    # 查询客户信息
    # data = Customer().query_customer(page=10000)
    # 查询销售区域
    data = Customer().query_district()
    print(data)
