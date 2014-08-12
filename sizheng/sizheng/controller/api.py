#encoding=utf8
__author__ = 'yuan'
import sys
import tools

from sizheng import app
from flask import render_template,request,abort,jsonify
from sizheng.model.article import *
reload(sys)
sys.setdefaultencoding('utf8')

#非常重要！否则json会返回unicode,即\u00e4\xe2之类的东西
app.config['JSON_AS_ASCII']=False

@app.route('/sizheng-api.json')
def api():
    recent20=[]
    articles=Article().getNewest20()

    for article in articles:
	    recent={}
	    recent['id']=article.id
	    recent['title']=str(article.title).encode('utf8')
	    recent['publishTime']=article.publishTime
	    recent20.append(recent)
    





    return jsonify(recent20=recent20)
