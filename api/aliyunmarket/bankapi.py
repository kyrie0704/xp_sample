# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :  bankapi.py
@Time    :  2022/12/30 15:43
@Author  :  Kyrie
@Email   :  Kyrie.Lu@littlefreddie.com
@Version :  1.0
@License :  (C)Copyright 2021-2022
@Desc    :  None
"""
import traceback
import warnings

import requests
warnings.filterwarnings('ignore')


class BankApi:
    def __init__(self, app_code):
        self.appcode = app_code

    def search_bank_by_cardno(self, cardno):
        """
        卡号查询总行联行号
        https://market.aliyun.com/products/57000002/cmapi00052746.html#sku=yuncode4674600001
        :param  cardno: 银行卡号
        """
        host = 'https://qrybkcode.market.alicloudapi.com'
        path = '/lundear/qryCardInfo'
        params = "?cardno={}".format(cardno)
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
            return False, f"卡号查询总行联行号接口异常，error:{e}"
        print(f"bank_code: {cardno}, return:{json_data}")
        if str(json_data.get("error_code")) == "0":
            print(len(json_data.get("result")["data"]))
            return True, json_data
        else:
            return False, f"接口返回错误，return:{json_data}"

    def search_bank_by_cardno_v2(self, cardno):
        """
        银行卡归属地查询
        https://market.aliyun.com/products/56928004/cmapi00059971.html?spm=5176.product-detail.sidebar.7.3edf6b17TUQBRT&scm=20140722.C_cmapi00059971.P_146.MO_732-ST_4769-V_1-ID_cmapi00059971-OR_rec#sku=yuncode5397100001
        :param  cardno: 银行卡号
        {
        "code": 0,
        "desc": "成功",
        "data": {
            "bankCode": "308584000013", //总行联行号
            "bankId": "03080000", //银行编码
            "bankName": "招商银行", //银行名称
            "abbr": "CMB", //银行英文缩写
            "cardName": "银联IC普卡", //卡名称
            "cardType": "借记卡", //卡类型
            "cardBin": "621483", //卡bin
            "binLen": 6, //卡bin长度
            "area": "北京 - 北京", //卡所在地区
            "bankPhone": "95555", //银行电话
            "bankUrl": "https://www.cmbchina.com", //银行网址
            "bankLogo": "http://img.lundear.com/e4aa64.png" //银行logo
        }
    }
        """
        host = 'https://bankarea.market.alicloudapi.com'
        path = '/lundear/bankArea'
        params = "?cardno={}".format(cardno)
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
            return False, f"卡号查询总行联行号接口异常，error:{e}"
        print(f"bank_code: {cardno}, return:{json_data}")
        if str(json_data.get("error_code")) == "0":
            print(len(json_data.get("result")["data"]))
            return True, json_data
        else:
            return False, f"接口返回错误，return:{json_data}"


if __name__ == "__main__":
    code = "623668710000810656"
    res = BankApi(app_code='xxx').search_bank_by_cardno(code)
    # res = BankApi(app_code='cf4cd903530c48559f75fdf403ac4210').search_bank_by_cardno_v2(code)
    # print(res)
