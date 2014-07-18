__author__ = 'yuan'

from flask import *
from sizheng import app
import sizheng.model.article as db_article
import sizheng.model.user as db_user




@app.route('/article/<int:articleid>')
def viewArticle(articleid):
    article = db_article.Article().getArticle(articleid)
    if article:
        article.views += 1
        return render_template('article.html',article=article)
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
            return 'success'

        else:
            return 'invalid article'

    else:
        return render_template('publish.html')


@app.route('/article/list')
def listArticle():
    articles = db_article.Article().getArticleByAuthor(session['username'])
    return render_template('articlelist.html',articles=articles)

@app.route('/article/delete/<articleid>')
def deleteArticle(articleid):
    db_article.Article().deleteArticle(articleid)

    return redirect('/article/list')
@app.route('/article/update/<articleid>',methods=['GET','POST'])
def updateArticle(articleid):
    if request.method == 'GET':
        article = db_article.Article().getArticle(articleid)
        return render_template('articleUpdate.html',article=article)
    elif request.method == 'POST':
        title = request.form['title']
        author = session['username']
        content = request.form['article']
        category = request.form['category']
        if title and author and content and category:
            db_article.Article().updateArticle(category,articleid,title,content,author)
            return redirect('/article/list')
        else:
            return 'invalid article'
