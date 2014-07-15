__author__ = 'yuan'
from flask import *
from sizheng import app

import sizheng.model.article as db_article
import sizheng.model.user as db_user





@app.route('/')
def index():
      selectedArticlesInChannels = map(db_article.Article().listNewestOfArticles,map(db_article.Article().getArticleByCategoryid,range(5)))
      return render_template('sizheng.html',selectedArticlesInChannels=selectedArticlesInChannels)
    # return render_template('test.html')