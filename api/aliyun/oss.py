# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :  oss.py
@Time    :  2023/3/23 13:37
@Author  :  Kyrie
@Email   :  Kyrie.Lu@littlefreddie.com
@Version :  1.0
@License :  (C)Copyright 2021-2022
@Desc    :  阿里云oss模块封装
"""
import os
import shutil

import oss2


class AliyunOss:
    def __init__(self, access_key_id, access_key_secret, endpoint, bucket):
        self._access_key_id = access_key_id
        self._access_key_secret = access_key_secret
        self._endpoint = endpoint
        self._bucket = bucket
        self._auth = oss2.Auth(self._access_key_id, self._access_key_secret)
        # 创建bucket对象
        self._bucket = oss2.Bucket(self._auth, self._endpoint, self._bucket)

    def get_bucket_info(self):
        """
        获取bucket相关信息，如创建时间，访问Endpoint，Owner与ACL等。
        """
        return self._bucket.get_bucket_info()

    def get_file_list(self, prefix=""):
        """
        获取oss上面所有文件
        :param prefix: 文件前缀
        """
        file_list = []
        for obj in oss2.ObjectIterator(bucket=self._bucket, prefix=prefix):
            file_list.append(obj.key)
        return file_list

    def upload_file(self, local_file, remote_file=None):
        """
        将本地文件上传到oss
        :param local_file: 本地文件名
        :param remote_file: 远程文件名
        """
        resp = self._bucket.put_object_from_file(remote_file, local_file)
        if str(resp.status) == "200":
            return True
        return False

    def upload_file_object(self, remote_file, data, prefix=None):
        """
        文件上传
        :param remote_file: 上传到OSS的文件名
        :param data: 待上传的内容。 bytes，str或file-like object
        :param prefix: 存放路径
        """
        key = prefix + remote_file
        resp = self._bucket.put_object(key=key, data=data)
        if str(resp.status) == "200":
            return True
        return False

    def resumable_upload(self, local_file, remote_file=None):
        """
        断点续传上传
        实现中采用分片上传方式上传本地文件，缺省的并发数是 `oss2.defaults.multipart_num_threads` ，并且在
        本地磁盘保存已经上传的分片信息。如果因为某种原因上传被中断，下次上传同样的文件，即源文件和目标文件路径都
        一样，就只会上传缺失的分片。

        缺省条件下，该函数会在用户 `HOME` 目录下保存断点续传的信息。当待上传的本地文件没有发生变化，
        且目标文件名没有变化时，会根据本地保存的信息，从断点开始上传。

        使用该函数应注意如下细节：
            #. 如果使用CryptoBucket，函数会退化为普通上传

        :param local_file: 待上传本地文件名
        :param remote_file: 上传到用户空间的文件名
        """
        resp = oss2.resumable_upload(self._bucket, remote_file, local_file, multipart_threshold=100*1024)
        if str(resp.status) == "200":
            return True
        return False

    def multipart_upload(self, local_file, remote_file=None, remove=False):
        """
        分片上传（较大文件需要使用分片上传）
        :param local_file: 待上传本地文件名
        :param remote_file: 上传的文件名
        :param remove: 是否删除本地文件
        """
        # 设定分片大小，设我们期望的分片大小为128KB
        total_size = os.path.getsize(local_file)
        part_size = oss2.determine_part_size(total_size, preferred_size=128 * 1024)
        # 初始化分片上传，得到upload id
        upload_id = self._bucket.init_multipart_upload(remote_file).upload_id
        # 逐个上传分片
        with open(local_file, 'rb') as obj:
            parts = []
            part_number = 1
            offset = 0
            while offset < total_size:
                size_to_upload = min(part_size, total_size-offset)
                self._bucket.upload_part(remote_file, upload_id, part_number,
                                         oss2.SizedFileAdapter(obj, size_to_upload))
                offset += size_to_upload
                part_number += 1
            # 完成分片上传
            self._bucket.complete_multipart_upload(remote_file, upload_id, parts)
        # 删除本地文件
        if remove:
            os.remove(local_file)

    def get_object_to_file(self, remote_file, local_path, filename=None):
        """
        下载oss文件到本地
        :param remote_file: 远程文件名
        :param local_path: 本地存储路径
        :param filename: 本地文件名
        """
        try:
            if filename is None:
                filename = remote_file.split("/")[-1]
            local_file = os.path.join(local_path, filename)
            # 因为get_object()方法返回的是一个file-like object，所以可以直接用shutil.copyfileobj()做拷贝
            with open(oss2.to_unicode(local_file), 'wb') as f:
                shutil.copyfileobj(self._bucket.get_object(remote_file), f)
            return True
        except Exception as e:
            print(f"下载oss文件到本地失败，error:{e}")
            return False

    def get_object(self, remote_file):
        """
        获取oss文件的文件流
        :param remote_file: 远程文件名
        """
        try:
            # get_object()方法返回的是一个file-like object，使用read方式读取出文件流
            return self._bucket.get_object(remote_file).read()
        except Exception as e:
            print(f"获取oss文件的文件流失败，error:{e}")
            return False

    def delete_file(self, filename):
        """
        删除文件
        """
        resp = self._bucket.delete_object(filename)
        if str(resp.status) == "204":
            return True
        return False

    def batch_delete(self, filename_list):
        """
        批量删除文件
        :param filename_list: 文件名列表，不能为空 eg:[file1, file2, file3...]
        """
        resp = self._bucket.batch_delete_objects(filename_list)
        if str(resp.status) == "200":
            return True
        return False


if __name__ == "__main__":
    access_key_id_ = "xxx"
    access_key_secret_ = "xxx"
    endpoint_ = "oss-cn-shenzhen.aliyuncs.com"
    bucket_ = "lf-online-test"
    oss_obj = AliyunOss(access_key_id_, access_key_secret_, endpoint=endpoint_, bucket=bucket_)
    res = oss_obj.get_file_list(prefix="devops/")
    print(res)
