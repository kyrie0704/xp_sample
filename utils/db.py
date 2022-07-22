# -*- coding: utf-8 -*-
# @Author: Kyrie
# @Email: Kyrie.Lu@littlefreddie.com
# @Time: 2022/7/21 16:28
# @Desc: 生成数据库连接对象
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from conf.setting import config


# 使用单例，确保只创建一个对象，方法里对引擎做判断，确保只创建一个数据库引擎
class DB(object):
    _instance = None
    _engine = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self.url = config.database_uri
        self.pool_size = config.pool_size
        self.pool_recycle = config.pool_recycle

    def create_engine(self):
        if DB._engine is None:
            # 初始化数据库连接; 设置session回收时间
            DB._engine = create_engine(url=self.url,
                                       pool_size=self.pool_size,
                                       pool_recycle=self.pool_recycle
                                       )

    @property
    def get_session(self):
        self.create_engine()
        # 创建Session对象
        db = sessionmaker(bind=DB._engine)
        # 线程安全，基于本地线程实现每个线程用同一个session
        return scoped_session(db)


if __name__ == "__main__":
    session = DB().get_session
    print(session)
