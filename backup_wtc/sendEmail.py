#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Arthur:Timbaland
# Date:
import  sys
reload(sys)
sys.setdefaultencoding('utf8')
import smtplib
from email.mime.text import MIMEText

# 收件人列表
mail_namelist = ['rzglxt@xuanyuan.com.cn',]
# mail_namelist =["422033564@qq.com",'leixiangling@xuanyuan.com.cn']
# 发送方信息
mail_user = "rzglxt@xuanyuan.com.cn"
#口令
# mail_pass = "rlixtgnujleocagi"
mail_pass = "1234qwer"
#发送邮件
#title：标题
#conen：内容
def send_qq_email(title,conen):
    try:
        msg = MIMEText(str(conen),'plain','utf-8')
        #设置标题
        msg["Subject"] = title
        # 发件邮箱
        msg["From"] = mail_user
        #收件邮箱
        msg["To"] = ";".join(mail_namelist)
        # 设置服务器、端口
        # s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s = smtplib.SMTP_SSL("mail.xuanyuan.com.cn", 465)
        #登录邮箱
        s.login(mail_user, mail_pass)
        # 发送邮件
        s.sendmail(mail_user, mail_namelist, msg.as_string())
        s.quit()
        print("邮件发送成功!")
        return True
    except smtplib.SMTPException:
        print("邮件发送失败！")
        return False

if __name__ == '__main__':
    send_qq_email("没有邮箱人员",'ssd')
