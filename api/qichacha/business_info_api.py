# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :  business_info_api.py
@Time    :  2022/9/5 9:25
@Author  :  Kyrie
@Email   :  Kyrie.Lu@littlefreddie.com
@Version :  1.0
@License :  (C)Copyright 2021-2022
@Desc    :  工商信息api
"""
import requests
import time
import hashlib


class QichachaApi:
    def __init__(self, app_key, secret_key):
        self.app_key = app_key
        self.secret_key = secret_key

    def create_token(self, timestamp):
        """
        创建验证加密值token
        :param timestamp : 时间戳
        :return:
        """
        en = hashlib.md5()
        data = self.app_key + timestamp + self.secret_key
        en.update(data.encode(encoding='utf-8'))
        return en.hexdigest().upper()

    def get_enterprise_info(self, search_key, logger=None):
        """
        获取企业基本信息
        https://openapi.qcc.com/dataApi/430
        :param search_key : 搜索关键字（企业名称、统一社会信用代码、注册号）
        :param logger : 是否开启日志记录
        """
        req_address = "http://api.qichacha.com/ECIComplement/GetInfo"
        url = req_address + "?key=" + self.app_key + "&searchKey=" + search_key
        timestamp = str(int(time.time()))
        headers = {'Token': self.create_token(timestamp), 'Timespan': timestamp}

        try:
            response = requests.get(url=url, headers=headers).json()
        except Exception as e:
            response = None
            print(f"获取企业基本信息接口请求异常，error:{e}")
            return response
        # 是否需要日志记录
        if logger:
            logger.info(f"获取 {search_key} 企业信息，返回：{response}")
        if str(response.get("Status")) != '200':
            print(f"获取企业基本信息信息，search_key:{search_key}, result:{response}")
            return None
        return response

    def company_fuzzy_search(self, search_key, page_size=20, page_index=1, logger=None):
        """
        企业工商模糊搜索
        https://openapi.qcc.com/dataApi/886
        :param search_key : 搜索关键字（如企业名、人名、产品名等）
        :param page_size : 每页条数，默认为10，最大不超过20
        :param page_index : 页码，默认第一页
        :param logger : 是否开启日志记录
        """
        req_address = "http://api.qichacha.com/FuzzySearch/GetList"
        url = req_address + f"?key={self.app_key}&searchKey={search_key}&pageSize={page_size}&pageIndex={page_index}"
        timestamp = str(int(time.time()))
        headers = {'Token': self.create_token(timestamp), 'Timespan': timestamp}

        try:
            response = requests.get(url=url, headers=headers).json()
        except Exception as e:
            response = None
            print(f"获取企业基本信息接口请求异常，error:{e}")
            return response
        # 是否需要日志记录
        if logger:
            logger.info(f"获取 {search_key} 企业信息，返回：{response}")
        if str(response.get("Status")) != '200':
            print(f"获取企业基本信息信息，search_key:{search_key}, result:{response}")
            return None
        return response


if __name__ == "__main__":
    app_key_ = "xxx"
    secret_key_ = "xxx"
    qi = QichachaApi(app_key_, secret_key_)

    # search_key = "昆明云端益创广告有限公司"
    # res = qi.get_enterprise_info(search_key, token, timestamp)
    # print(res)

    secret_key_ = "汇丰银行"
    res = qi.company_fuzzy_search(secret_key_)
    print(res)
