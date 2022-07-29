# -*- coding: utf-8 -*-
# @Author: Kyrie
# @Email: Kyrie.Lu@littlefreddie.com
# @Time: 2022/7/29 15:07
# @Desc: 邮件发送器
import os.path
import re
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

from conf.mail_cfg import mail_config, cate_list


class Email:
    def __init__(self):
        self.host = mail_config.get("host")
        self.sender = mail_config.get("sender")
        self.mail_license = mail_config.get("license")
        self.cate_list = cate_list

    def send_mail(self, receiver_list, subject, body_dict, cate):
        """
        发送邮件
        :param receiver_list : 邮件接收人列表
        :param subject : 邮件主题
        :param body_dict: {"project": xxx, "module": xxx, "msg": xxx}
        :param cate: 邮件分类(error异常、warning告警、info通知)
        """
        if cate not in self.cate_list:
            return "请选择告警类型--error,warning或者info"

        # 处理邮件信息
        content = self.handle_body(body_dict, cate)

        mm = MIMEMultipart('related')

        mm["From"] = "littlefreddie<" + self.sender + ">"
        mm["To"] = ";".join(receiver_list)
        # 设置邮件主题
        mm["Subject"] = Header(subject, 'utf-8')

        # 构造文本：正文内容，文本格式，编码方式
        message_text = MIMEText(content, "html", "utf-8")
        # 向MIMEMultipart对象中添加文本对象
        mm.attach(message_text)

        stp = None
        try:
            # 创建smtp对象
            stp = smtplib.SMTP_SSL(self.host)
            stp.login(self.sender, self.mail_license)
            stp.sendmail(self.sender, receiver_list, mm.as_string())
            stp.quit()
            print("邮件发送成功...")
        except Exception as e:
            if stp:
                stp.quit()
            print(e)
            print("邮件发送失败...")
            print("收件人为：{},主题为：{},内容为：{}".format(receiver_list, subject, content))

    @staticmethod
    def handle_body(body_dict, cate):
        """
        处理邮件内容
        :param body_dict: {"project": xxx, "module": xxx, "msg": xxx}
        :param cate: 邮件分类(error异常、warning告警、info通知)
        :return : 邮件正文内容
        """
        now_time = time.strftime("%Y{0}%m{1}%d{2}%H{3}%M{4}", time.localtime(time.time())).format('年', '月', '日', '时',
                                                                                                  '分')
        file_name = cate + ".html"
        file = os.path.join("../template", file_name)
        with open(file, "r", encoding="utf-8") as f:
            html = f.read()
        print(html)
        content = ""
        if body_dict.get("project", ""):
            content += body_dict.get("project", "")
        if body_dict.get("module", ""):
            content += body_dict.get("module", "")

        try:
            info = html % (content, body_dict.get("msg"), now_time)
        except Exception as e:
            print(e)
            return body_dict.get("project") + body_dict.get("module") + body_dict.get("msg")

        return info

    @staticmethod
    def check_email(email):
        """
        验证邮箱格式是否正确
        :param email: 邮箱
        """
        if len(email) <= 7:
            return False
        if not re.compile(r'([A-Za-z\d]+[.-_])*[A-Za-z\d]+@[A-Za-z\d-]+(\.[A-Z|a-z]{2,})+'):
            return False
        return True


if __name__ == "__main__":
    receiver_list_ = ["kyrie.lu@littlefreddie.com"]
    subject_ = "测试邮件发送"
    body_dict_ = {"project": "主数据项目", "module": "数据分析模块", "msg": "分析数据异常"}
    cate_ = "info"
    Email().send_mail(receiver_list_, subject_, body_dict_, cate_)
