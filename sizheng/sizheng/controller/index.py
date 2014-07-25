__author__ = 'yuan'
from flask import *
from sizheng import app
import sizheng.config as config
import sizheng.model.article as db_article
import sizheng.model.user as db_user





@app.route('/')
@app.route('/page/<int:pageNum>')
def index(pageNum=1):

      # selectedArticlesInChannels = map(db_article.Article().listNewestOfArticles,map(db_article.Article().getArticleByCategoryid,range(config.CATEGORY_COUNT)))
      allArticles = db_article.Article().getAllArticles()
      pages,hotArticles = db_article.Article().cutArticlesAsPages(db_article.Article().getHotArticles(),11,1)

      pages,articles = db_article.Article().cutArticlesAsPages(allArticles,20,pageNum)
      return render_template('index/list.html',articles=articles,hotArticles=hotArticles,totalPages=pages,currentPage=pageNum)

