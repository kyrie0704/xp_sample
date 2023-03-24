# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :  geo_place_api.py
@Time    :  2022/9/26 14:03
@Author  :  Kyrie
@Email   :  Kyrie.Lu@littlefreddie.com
@Version :  1.0
@License :  (C)Copyright 2021-2022
@Desc    :  高德  搜索POI 2.0
"""
import requests


class GeoPlaceApi:
    def __init__(self, key):
        self.key = key
        self.output = "JSON"

    def get_place_info_v5(self, params: dict):
        """
        搜索POI 关键字搜索
        https://lbs.amap.com/api/webservice/guide/api/newpoisearch
        :param: params 传入参数 {"types": "指定地点类型", "page_size": "当前分页展示的数据条数", "region": "搜索区划",
                                "city_limit":"指定城市数据召回限制", "page_num": "请求第几分页"}
        """
        if not params.get("types"):
            return False, "缺少地点类型"

        req_address = "https://restapi.amap.com/v5/place/text"
        req_params = ""
        for k, v in params.items():
            req_params += "&" + str(k) + "=" + str(v)
        url = req_address + "?key=" + self.key + "&output=" + self.output + req_params

        try:
            response = requests.get(url=url)
        except Exception as e:
            return False, f"请求失败，error:{e}"

        resp = response.json()
        if str(resp.get("status")) == "0":
            return False, f"返回错误，return:{resp.get('info')}"
        return True, response.json()

    def get_place_info_v3(self, params: dict):
        """
        搜索POI 2.0 关键字搜索
        https://lbs.amap.com/api/webservice/guide/api/search
        :param: params 传入参数 {"types": "指定地点类型", "offset": "当前分页展示的数据条数", "city": "搜索区划",
                                "city_limit":"指定城市数据召回限制", "page": "请求第几分页"}
        """
        if not params.get("types"):
            return False, "缺少地点类型"

        params.update({"extensions": "all"})

        req_address = "https://restapi.amap.com/v3/place/text"
        req_params = ""
        for k, v in params.items():
            req_params += "&" + str(k) + "=" + str(v)
        url = req_address + "?key=" + self.key + "&output=" + self.output + req_params

        try:
            response = requests.get(url=url)
        except Exception as e:
            return False, f"请求失败，error:{e}"

        resp = response.json()
        if str(resp.get("status")) == "0":
            return False, f"返回错误，return:{resp.get('info')}"
        return True, response.json()


if __name__ == "__main__":
    key_ = "xxx"
    # dict_ = {
    #     "types": "160100",
    #     "region": "110101",
    #     "city_limit": True,
    #     "page_size": 20,
    #     "page_num": 1
    # }
    dict_ = {'types': '060100', 'city': '361102', 'city_limit': True, 'offset': 20, 'page': 6, 'extensions': 'all'}
    geo = GeoPlaceApi(key_)
    # status, data = geo.get_place_info_v5(dict_)
    status, data = geo.get_place_info_v5(dict_)
    print(data)
    # print(data.get("pois"))
    """
    {'status': '1', 'info': 'OK', 'infocode': '10000', 'count': '1', 
    'geocodes': 
    [
    {'formatted_address': '广西壮族自治区桂林市龙胜各族自治县龙胜镇北岸', 'country': '中国', 'province': '广西壮族自治区', 
    'citycode': '0773', 'city': '桂林市', 'district': '龙胜各族自治县', 'township': [], 'neighborhood': {'name': [], 
    'type': []}, 'building': {'name': [], 'type': []}, 'adcode': '450328', 'street': [], 'number': [], 
    'location': '110.015832,25.803168', 'level': '热点商圈'}
    ]
    }
    """
