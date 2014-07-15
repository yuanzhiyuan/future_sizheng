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


@app.route('/article/add',methods=['POST'])
def addArticle():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        article = request.form['article']
        category = request.form['category']
        if title and author and article and category:
            db_article.Article().addArticle(category,title,article,author)
        else:
            'invalid article'

    return redirect('/user/'+session['username'])


