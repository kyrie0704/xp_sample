# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :  geocode_api.py
@Time    :  2022/9/19 16:41
@Author  :  Kyrie
@Email   :  Kyrie.Lu@littlefreddie.com
@Version :  1.0
@License :  (C)Copyright 2021-2022
@Desc    :  地理/逆地理编码
"""
import requests


class GeoApi:
    def __init__(self, key):
        self.key = key
        self.output = "JSON"

    def get_geocode(self, params: dict):
        """
        获取地理编码信息
        https://lbs.amap.com/api/webservice/guide/api/georegeo
        :param: params 传入参数 {"address": "必要", "city": "非必要"}
        """
        if not params.get("address"):
            return False, "缺少地址信息"

        req_address = "https://restapi.amap.com/v3/geocode/geo"
        req_params = ""
        for k, v in params.items():
            req_params += "&" + str(k) + "=" + str(v)
        url = req_address + "?key=" + self.key + "&output=" + self.output + req_params

        try:
            response = requests.get(url=url)
        except Exception as e:
            return False, f"获取地理编码信息请求失败，error:{e}"

        resp = response.json()
        if str(resp.get("status")) == "0":
            return False, f"获取地理编码信息失败，return:{resp.get('info')}"
        return True, response.json()

    def get_re_geocode(self, params: dict):
        """
        获取逆地理编码信息
        https://lbs.amap.com/api/webservice/guide/api/georegeo
        :param: params 传入参数 {"location": "经纬度坐标"}
        """
        if not params.get("location"):
            return False, "缺少经纬度信息"

        req_address = "https://restapi.amap.com/v3/geocode/regeo"
        url = req_address + "?key=" + self.key + "&location=" + params.get("location")

        try:
            response = requests.get(url=url)
        except Exception as e:
            return False, f"获取逆地理编码信息请求失败，error:{e}"

        resp = response.json()
        if str(resp.get("status")) == "0":
            return False, f"获取逆地理编码信息失败，return:{resp.get('info')}"
        return True, response.json()


if __name__ == "__main__":
    key_ = "xxx"
    geo = GeoApi(key_)

    # 获取地理编码
    # dict_ = {
    #     "address": "邮政银行石狮市九二支行"
    # }
    # status, data = geo.get_geocode(dict_)
    # print(data)

    # 获取逆地理编码
    dict_ = {
        "location": "124.074694,40.450115"
    }
    status, data = geo.get_re_geocode(params=dict_)
    print(data)
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
