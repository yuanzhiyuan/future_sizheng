__author__ = 'yuan'
from sizheng import app
from flask import render_template
from sizheng.controller.tools import *

@app.route('/test')
def test():
    send_mail(['707699544@qq.com'],'test','testcontent')
    #User().add('haha','002899','aaa','aaaaaaa')
    return render_template('login.html')