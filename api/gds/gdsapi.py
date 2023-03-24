# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :  gdsapi.py
@Time    :  2023/3/13 17:29
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


class GDSApi:
    def __init__(self):
        self.host = "https://bff.gds.org.cn/gds/searching-api/ImportProduct/GetImportProductDataForGtin"

    def search_bar_code(self, bar_code, page_size=30, page_index=1):
        """
        查条码
        https://www.gds.org.cn/#/barcodeList/index?type=barcode&keyword=5060403119049
        :param  bar_code: 商品条码
        :param  page_size: 每页条数
        :param  page_index: 页码
        """
        url = f"{self.host}?PageSize={page_size}&PageIndex={page_index}&Gtin={bar_code}&AndOr=0"

        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IkNFOTk2QzBDQzg1MzQ4MkEzMzQxNkVBOUUxQ0E3NkVERjYzMUJCODNSUzI1NiIsInR5cCI6ImF0K2p3dCIsIng1dCI6InpwbHNETWhUU0NvelFXNnA0Y3AyN2ZZeHU0TSJ9.eyJuYmYiOjE2Nzg3NTkyODAsImV4cCI6MTY3ODc2NjQ4MCwiaXNzIjoiaHR0cHM6Ly9wYXNzcG9ydC5nZHMub3JnLmNuIiwiY2xpZW50X2lkIjoidnVlanNfY29kZV9jbGllbnQiLCJzdWIiOiIxNDI2MzgzIiwiYXV0aF90aW1lIjoxNjc4NzU5Mjc5LCJpZHAiOiJsb2NhbCIsInJvbGUiOiJTeXN0ZW1NZW1iZXJDYXJkVXNlciIsIlVzZXJJbmZvIjoie1wiVXNlck5hbWVcIjpcIjE1NjM2NjNcIixcIkJyYW5kT3duZXJJZFwiOjczMjAyNyxcIkJyYW5kT3duZXJOYW1lXCI6XCLpmLPlhYnpuqbnlLDotLjmmJMo5rex5ZyzKeaciemZkOWFrOWPuFwiLFwiR2NwQ29kZVwiOltcIjY5NzE5ODY5OFwiXSxcIlVzZXJDYXJkTm9cIjpcIjE1NjM2NjNcIixcIklzUGFpZFwiOmZhbHNlLFwiQ29tcGFueU5hbWVFTlwiOlwiXCIsXCJDb21wYW55QWRkcmVzc0NOXCI6XCLmt7HlnLPluILnpo_nlLDljLrovablhazlupnlpKnlkInlpKfljqYzQTItMSAzQTItMlwiLFwiQ29udGFjdFwiOlwi6IyD5oCd5rWpXCIsXCJDb250YWN0VGVsTm9cIjpcIjE1NjI2MjEwNTMwXCIsXCJHY3BMaWNlbnNlSG9sZGVyVHlwZVwiOlwiSDYzOTlcIixcIkxlZ2FsUmVwcmVzZW50YXRpdmVcIjpcIuS9leiZuVwiLFwiVW5pZmllZFNvY2lhbENyZWRpdENvZGVcIjpcIjkxNDQwMzAwMDg3ODM2NDY3NFwifSIsIlY0VXNlckluZm8iOiJ7XCJVc2VyTmFtZVwiOlwiMTU2MzY2M1wiLFwiRW1haWxcIjpudWxsLFwiUGhvbmVcIjpudWxsLFwiQ2FyZE5vXCI6XCIxNTYzNjYzXCJ9IiwianRpIjoiNDUyRDcxM0IyNDZEQjQyQURGRkExQkRDNEIyQUE1QkUiLCJzaWQiOiIwM0ZGRUYwMUVCMTFGOTAyOTg3OTIzOTVFQjRFREExRSIsImlhdCI6MTY3ODc1OTI4MCwic2NvcGUiOlsib3BlbmlkIiwicHJvZmlsZSIsImFwaTEiLCJvZmZsaW5lX2FjY2VzcyJdLCJhbXIiOlsicHdkIl19.SpGGRIGP3nJfJH0mHWE2RPuUBxUkYPC_wIBxg4-3rarHet1GVFvXvpmEXVajzzrE57n9t49QjQ9s1TqOq1buUQs9vMKWJGgWEzocWoB1xPArHwXhTrj4PwYHIn0YupsHPe4MizfNwXhYRmaAXaczmOlC9_Fh6XbES7kUhFVJAjSHUx2GA944FkfX0G1JXpV-VkjqOPq2T_s6VfYpMoe1jAYNkLrY1qsT7OFpbajxcscCV4WTpYzGUFaYnioTyCkt1N4o7Id-Zp7jftO3mda3ejcnKDNIaKX-dWvsUx-ztuv6xem2XN65d_soXZNV-7eeDww8_wJGGuyR-jc_4200fQ'
        }

        try:
            resp = requests.get(url=url, headers=headers)
            json_data = resp.json()
        except Exception as e:
            print(traceback.print_exc())
            return False, f"条码查询接口异常，error:{e}"
        if json_data.get("Msg") != "Success":
            print(f"条码查询失败，返回：{json_data.get('Msg')}")
            return False, json_data.get('Msg')
        return True, json_data.get("Data").get("Items")


if __name__ == "__main__":
    res = GDSApi().search_bar_code(bar_code="5060403119049")
    print(res)
