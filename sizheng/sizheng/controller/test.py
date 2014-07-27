__author__ = 'yuan'
from sizheng import app
from flask import *
from sizheng.controller.tools import *

@app.route('/test')
def test():
    # send_mail(['707699544@qq.com'],'test','testcontent')
    # #User().add('haha','002899','aaa','aaaaaaa')
    # return render_template('login.html')
    data=request.cookies.get('username')

    resp = make_response(render_template('test.html',data=data))
    # resp.delete_cookie('username')
    return resp