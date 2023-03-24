# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :  place_api.py
@Time    :  2022/11/8 16:07
@Author  :  Kyrie
@Email   :  Kyrie.Lu@littlefreddie.com
@Version :  1.0
@License :  (C)Copyright 2021-2022
@Desc    :  百度地图  地点检索V2.0
"""
import requests


class BaiduPlaceApi:
    def __init__(self, key):
        self.key = key
        self.output = "json"

    def get_place_info(self, params: dict):
        """
        行政区划区域检索
        https://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi
        :param: params 传入参数 {"query": "指定地点类型", "page_size": "当前分页展示的数据条数", "region": "搜索区划",
                                "city_limit":"指定城市数据召回限制", "page_num": "请求第几分页"}
        """
        req_address = "https://api.map.baidu.com/place/v2/search"
        req_params = ""
        for k, v in params.items():
            req_params += "&" + str(k) + "=" + str(v)
        url = req_address + "?ak=" + self.key + "&output=" + self.output + req_params
        print(url)
        try:
            response = requests.get(url=url)
        except Exception as e:
            return False, f"请求失败，error:{e}"
        print(response.json())
        # resp = response.json()
        # if str(resp.get("status")) == "0":
        #     return False, f"返回错误，return:{resp.get('info')}"
        # return True, response.json()


if __name__ == "__main__":
    key_ = "xxx"
    dict_ = {'query': '爱婴岛', 'tag': '购物', 'region': '340', 'city_limit': True, 'page_size': 5, 'page_num': 0,
             'scope': '2'}
    geo = BaiduPlaceApi(key_)
    # status, data = geo.get_place_info_v5(dict_)
    geo.get_place_info(dict_)
    # status, data = geo.get_place_info(dict_)
    # print(data)
