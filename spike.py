import smtplib
# from email.mime.text import MIMEText
# from email.header import Header
#
# # 第三方 SMTP 服务
# mail_host = "smtp.163.com"  # 设置服务器
# mail_user = "13501077762@163.com"  # 用户名
# mail_pass = "yinglong123"  # 口令
#
# sender = '13501077762@163.com'
# receivers = ['liuxiwang@kong.net','gaoyinglong@kong.net']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
#
# message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
# message['From'] = Header("菜鸟教程", 'utf-8')
# message['To'] = Header("测试", 'utf-8')
#
# subject = 'Python SMTP 邮件测试'
# message['Subject'] = Header(subject, 'utf-8')
#
# try:
#     smtpObj = smtplib.SMTP()
#     smtpObj.connect(mail_host)  # 25 为 SMTP 端口号
#     smtpObj.login(mail_user, mail_pass)
#     smtpObj.sendmail(sender, receivers, message.as_string())
#     print ("邮件发送成功")
# except smtplib.SMTPException:
#     print ("Error: 无法发送邮件")
#
# import random
#
# def GBK2312():
#     name = '测试'
#     for x in range(3):
#         head = random.randint(0xb0, 0xf7)
#         body = random.randint(0xa1, 0xf9)   # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
#         val = f'{head:x}{body:x}'
#         str = bytes.fromhex(val).decode('gb2312')
#         name += str
#     return name
#
# print(GBK2312())

# a = '  ab\n  c  '
# b = a.strip()
# c = b.replace('\n','').replace('\r','')
#
# print(c)

if 0:
    print(1)