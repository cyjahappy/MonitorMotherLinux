import smtplib
from email.mime.text import MIMEText
from email.header import Header


class Mail:
    # 第三方 SMTP 服务
    __mail_host = "smtp.qq.com"  # 设置服务器
    __mail_user = "821659763@qq.com"  # 用户名
    __mail_pass = ""  # 邮箱密码
    __sender = '821659763@qq.com'
    __receivers = ['swe1609034@xmu.edu.my']  # 接收的邮件地址

    def __init__(self):
        print('Start sending email from ', self.__sender, 'to ', self.__receivers)

    def send_mails(self, content):
        message = MIMEText(content, 'plain', 'utf-8')
        message['From'] = Header("检测员", 'utf-8')
        message['To'] = Header("cyj", 'utf-8')

        subject = 'Linux系统监测'
        message['Subject'] = Header(subject, 'utf-8')

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.__mail_host, 25)  # 25 为 SMTP 端口号
            smtpObj.login(self.__mail_user, self.__mail_pass)
            smtpObj.sendmail(self.__sender, self.__receivers, message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")

