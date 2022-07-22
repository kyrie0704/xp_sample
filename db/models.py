# -*- coding: utf-8 -*-
# @Author: Kyrie
# @Email: Kyrie.Lu@littlefreddie.com
# @Time: 2022/7/21 16:28
# @Desc: 数据库模型类
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, SmallInteger


Base = declarative_base()


class BankBranchInfo(Base):
    __tablename__ = "bank_branch_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bank_name = Column(String(255), nullable=False, default="", comment="总行名称")
    bank_code = Column(String(255), nullable=False, default="", comment="银行联行号")
    bank_branch_name = Column(String(255), nullable=False, default="", comment="支行名称")
    country = Column(String(255), nullable=False, default="", comment="银行注册的国家或地区")
    province = Column(String(255), nullable=False, default="", comment="银行所在省份")
    city = Column(String(255), nullable=False, default="", comment="银行所在城市")
    address = Column(String(255), nullable=False, default="", comment="地址")
    telephone = Column(String(255), nullable=False, default="", comment="电话号码")
    postcode = Column(String(255), nullable=False, default="", comment="邮政编码")
    status = Column(SmallInteger, nullable=False, default=1, comment='可用状态(0失效,1正常)')
    create_time = Column(DateTime, comment='创建时间')
    modify_time = Column(DateTime, comment='更新时间')


class PostCodeInfo(Base):
    __tablename__ = "post_code_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    postcode = Column(String(255), nullable=False, default="", comment="邮政编码")
    province = Column(String(255), nullable=False, default="", comment="银行所在省份")
    city = Column(String(255), nullable=False, default="", comment="银行所在城市")
    town = Column(String(255), nullable=False, default="", comment="县")
    address = Column(String(255), nullable=False, default="", comment="乡")
