# -*- coding: utf-8 -*-
# @Author: Kyrie
# @Email: Kyrie.Lu@littlefreddie.com
# @Time: 2022/7/29 14:55
# @Desc: 邮件配置信息
"""
outlook邮箱获取授权码  https://www.vpsss.net/28088.html
常用邮箱SMTP服务器:
    outlook:       smtp.office365.com（SSL启用端口：587）
    网易邮箱:       smtp.163.com（端口：25）
    QQ邮箱:        smtp.qq.com（端口：25）
    谷歌邮箱:       smtp.gmail.com（SSL启用端口：587）
    阿里云邮箱:     smtp.aliyun.com（SSL加密端口：465；非加密端口：25）
"""
mail_config = {
    "host": "",
    "port": 25,
    "sender": "",
    "license": ""
}

cate_list = ["info", "warning", "error"]
