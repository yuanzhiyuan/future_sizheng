#encoding:utf8
import time
import smtplib
import sizheng.config as config
from sizheng import app
from email.mime.text import MIMEText
from flask import request


@app.template_filter('timeformat')
def timeformat_filter(t,formatstr):
    return time.strftime(formatstr,time.localtime(int(t)))

def send_mail(to_list,title,content):
    me="707699544<707699544@qq.com>"
    msg = MIMEText(content,_subtype='plain',_charset='UTF-8')
    msg['Subject'] = title
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(config.MailHost)
        server.login(config.MailUser,config.MailPass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False

    finally:
        print 'mail been send'