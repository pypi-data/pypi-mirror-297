# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-09-23 16:03
# @Author : 毛鹏
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 邮箱配置
smtp_server = 'smtp.qq.com'
smtp_port = 587  # 或 465
sender_email = '729164035@qq.com'
sender_password = 'lqfzvjbpfcwtbecg'
receiver_email = '729164035@qq.com'

# 创建邮件内容
subject = '测试邮件'
body = '这是一封通过Python发送的测试邮件。'

# 创建MIMEText对象
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

try:
    # 连接到SMTP服务器并发送邮件
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # 启用TLS加密
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print('邮件发送成功！')
except Exception as e:
    print(f'邮件发送失败: {e}')
