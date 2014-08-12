__author__ = 'yuan'
from sizheng import app
from flask import *
from sizheng.controller.tools import *
import sizheng.model.article as db_article

@app.route('/test')
def test():
    # send_mail(['707699544@qq.com'],'test','testcontent')
    # #User().add('haha','002899','aaa','aaaaaaa')
    # return render_template('login.html')
    # data=request.cookies.get('username')
    articles=db_article.Article().getNewest20()
    resp = make_response(render_template('test.html',data=articles))
    # resp.delete_cookie('username')

    return resp