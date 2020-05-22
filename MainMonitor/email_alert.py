import time
from .send_email import *

time_stamp = 0.0


def email_alert():
    global time_stamp
    if time_stamp == 0.0:
        try:
            mail = Mail()
            mail.send_mails('The Linux server is overload')
        except Exception as e:
            print(e)
        time_stamp = time.time()
    else:
        time_stamp_now = time.time()
        # 上一次发送了邮件之后, 隔600秒才能发送下一次邮件
        if (time_stamp_now - time_stamp) >= 600:
            time_stamp = time_stamp_now
            try:
                mail = Mail()
                mail.send_mails('The Linux server is overload')
            except Exception as e:
                print(e)
        else:
            pass
