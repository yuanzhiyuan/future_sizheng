#encoding=utf8
__author__ = 'yuan'

from flask import *
from sizheng import app
import sizheng.config as config
from sizheng.controller.tools import *
import sizheng.model.article as db_article
import sizheng.model.user as db_user




@app.route('/article/<int:articleid>')
def viewArticle(articleid):
    article = db_article.Article().getArticle(articleid)

    if article:
        # return render_template('test.html')
        article.views+=1
        #session不能存储article对象。。所以存储了id
        if db_article.Article().isVerified(articleid):
            if 'recentRead' in session:

                if articleid in session['recentRead']:
                    session['recentRead'].remove(articleid)
                session['recentRead'].append(articleid)
            else:
                session['recentRead'] = [articleid]
        else:
            if 'recentRead' not in session:
                session['recentRead'] = []
        #反转过来，刚看过的文章排在最上面
        reversedArticle = sorted(session['recentRead'],reverse=True)
        # reversedArticle = session['recentRead']
        if len(session['recentRead'])<=11:

            recentRead = map(db_article.Article().getArticle,reversedArticle)
        else:
            recentRead = map(db_article.Article().getArticle,reversedArticle[:11])
        pages,hotArticles = db_article.Article().cutArticlesAsPages(db_article.Article().getHotArticles(),11,1)
        return render_template('index/article.html',article=article,hotArticles=hotArticles,recentRead=recentRead)
    else:
        return abort(404)


@app.route('/article/add',methods=['POST','GET'])
def addArticle():
    if request.method == 'POST':
        title = request.form['title']
        author = session['username']
        article = request.form['article']
        category = request.form['category']
        if title and author and article and category:
            db_article.Article().addArticle(category,title,article,author)
            try:
                send_mail([config.Admin],'有人发表了文章','文章作者:{author},文章标题:{title}'.format(author=author,title=title))
            finally:
                return '发表成功'

        else:
            return '无效的文章'

    else:
        return render_template('user/publish.html')


@app.route('/article/list')
def listArticle():
    articles = db_article.Article().getArticleByAuthor(session['username'])
    return render_template('user/articlelist.html',articles=articles)

@app.route('/article/delete/<articleid>')
def deleteArticle(articleid):
    db_article.Article().deleteArticle(articleid)

    return redirect('/article/list')
@app.route('/article/update/<articleid>',methods=['GET','POST'])
def updateArticle(articleid):
    if request.method == 'GET':
        article = db_article.Article().getArticle(articleid)
        return render_template('user/articleUpdate.html',article=article)
    elif request.method == 'POST':
        title = request.form['title']
        author = session['username']
        content = request.form['article']
        category = request.form['category']
        if title and author and content and category:
            db_article.Article().updateArticle(category,articleid,title,content,author)
            article = db_article.Article().getArticle(articleid)
            article.state = 0
            return '更新成功'
        else:
            return '无效的文章'
