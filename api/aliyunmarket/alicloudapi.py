# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :  alicloudapi.py
@Time    :  2022/10/17 10:25
@Author  :  Kyrie
@Email   :  Kyrie.Lu@littlefreddie.com
@Version :  1.0
@License :  (C)Copyright 2021-2022
@Desc    :  阿里云市场api
"""
import ast
import traceback
import warnings

from urllib.parse import quote
from urllib import request
import requests
warnings.filterwarnings('ignore')


class AliCloudApi:
    def __init__(self, app_code):
        self.appcode = app_code

    def get_geo_data(self, address="", batch=False, output='JSON'):
        """
        获取地址位置
        https://market.aliyun.com/products/57002002/cmapi020535.html
        :param address: 结构化地址信息。如需解析多个地址，使用"|"进行间隔，并将batch参数设置为True
        :param batch: 批量查询控制。设置为true时进行批量查询操作
        :param output: 返回数据格式。可选择json/xml
        :return
        """
        host = 'http://geo.market.alicloudapi.com'
        path = '/v3/geocode/geo'
        params = '?address={}&batch={}&output={}'.format(quote(address), batch, output)
        url = host + path + params
        req = request.Request(url)
        req.add_header('Authorization', 'APPCODE ' + self.appcode)

        try:
            response = request.urlopen(req)
            content = response.read()
        except Exception as e:
            print(traceback.print_exc())
            return False, f"获取地址位置异常, error:{e}"
        if not content:
            return False, f"获取地理位置数据异常，返回:{content}"
        data = ast.literal_eval(content.decode())
        # print(data)
        if data.get('status') == '1':
            return True, data
        else:
            return False, f"获取地理位置数据失败，返回:{data}"

    def zipcode_query(self, zipcode):
        """
        邮编查地址
        https://market.aliyun.com/products/57126001/cmapi033506.html
        :param zipcode: 邮政编码
        """
        host = 'https://jisuyb.market.alicloudapi.com'
        path = '/zipcode/query'
        params = "?zipcode={}".format(zipcode)
        url = host + path + params

        headers = {
            'Authorization': 'APPCODE ' + self.appcode,
            'Content-Type': 'application/json; charset=UTF-8'
        }

        try:
            resp = requests.get(url=url, headers=headers, verify=False)
            json_data = resp.json()
        except Exception as e:
            print(traceback.print_exc())
            return False, f"邮编查地址接口异常，error:{e}"
        print(f"postcode: {zipcode}, return:{json_data}")
        if str(json_data.get("status")) == "0":
            return True, json_data
        else:
            return False, f"接口返回错误，return:{json_data}"

    def all_area(self):
        """
        获取全部区域接口
        """
        host = 'https://jisuarea.market.alicloudapi.com'
        path = '/area/all'
        url = host + path

        headers = {
            'Authorization': 'APPCODE ' + self.appcode
        }
        resp = requests.get(url=url, headers=headers)
        print(resp.json())
        return resp.json()

    def search_company(self, page, search_key):
        """
        企业关键词搜索
        https://market.aliyun.com/products/57000002/cmapi031025.html
        """
        host = 'https://bankpros.market.alicloudapi.com'
        path = '/searchCompany'
        params = "?com={}&page={}&query=all".format(page, search_key)
        url = host + path + params

        headers = {
            'Authorization': 'APPCODE ' + self.appcode,
            'Content-Type': 'application/json; charset=UTF-8'
        }

        try:
            resp = requests.get(url=url, headers=headers, verify=False)
            json_data = resp.json()
        except Exception as e:
            print(traceback.print_exc())
            return False, f"企业关键词搜索接口异常，error:{e}"
        print(f"search_key: {search_key}, return:{json_data}")
        if str(json_data.get("error_code")) == "0":
            print(len(json_data.get("result")["data"]))
            return True, json_data
        else:
            return False, f"接口返回错误，return:{json_data}"

    def search_bank_by_bank_code(self, bank_code):
        """
        联行号查询支行信息
        https://market.aliyun.com/products/57000002/cmapi00052746.html
        :param  bank_code: 联行号
        """
        host = 'https://qrybkcode.market.alicloudapi.com'
        path = '/lundear/qryshh'
        params = "?bankcode={}".format(bank_code)
        url = host + path + params

        headers = {
            'Authorization': 'APPCODE ' + self.appcode,
            'Content-Type': 'application/json; charset=UTF-8'
        }

        try:
            resp = requests.get(url=url, headers=headers, verify=False)
            json_data = resp.json()
        except Exception as e:
            print(traceback.print_exc())
            return False, f"企业关键词搜索接口异常，error:{e}"
        print(f"bank_code: {bank_code}, return:{json_data}")
        if str(json_data.get("error_code")) == "0":
            print(len(json_data.get("result")["data"]))
            return True, json_data
        else:
            return False, f"接口返回错误，return:{json_data}"


if __name__ == "__main__":
    add = "中国银行股份有限公司张家港大新支行"
    res = AliCloudApi(app_code='xxx').get_geo_data(address=add)
    print(res)
    # zipcode = "51230"
    # res = AliCloudApi(app_code='cf4cd903530c48559f75fdf403ac4210').zipcode_query(zipcode)
    # print(res)
    key_ = "广发银行"
    # key_ = "深圳农村商业银行"
    # key_ = "法国兴业银行"
    # code = "102100099996"
    # res = AliCloudApi(app_code='cf4cd903530c48559f75fdf403ac4210').search_bank_by_bank_code(code)
    # print(res)
