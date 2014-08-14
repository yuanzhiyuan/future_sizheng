#encoding=utf8
__author__ = 'yuan'

from flask import *
from sizheng import app
import sizheng.config as config
from sizheng.controller.tools import *
import sizheng.model.article as db_article
import sizheng.model.user as db_user
from sizheng.controller.auth import *




@app.route('/article/<int:articleid>')
def viewArticle(articleid):
    article = db_article.Article().getArticle(articleid)

    if article:

        # return render_template('test.html')
        article.views+=1
        #session不能存储article对象。。所以存储了id
        if db_article.Article().isVerified(articleid):
            if request.cookies.get('recentRead'):
                recentRead = map(int,request.cookies.get('recentRead').split('***'))
                if articleid in recentRead:
                    recentRead.remove(articleid)
                recentRead.append(articleid)
            else:
                recentRead = [articleid]

            # if 'recentRead' in session:
            #
            #     if articleid in session['recentRead']:
            #         session['recentRead'].remove(articleid)
            #     session['recentRead'].append(articleid)
            # else:
            #     session['recentRead'] = [articleid]
        else:
            return '这篇文章未被审核'
        #反转过来，刚看过的文章排在最上面
        reversedArticle = sorted(recentRead,reverse=True)
        # reversedArticle = session['recentRead']
        if len(recentRead)<=11:

            recent = map(db_article.Article().getArticle,reversedArticle)
        else:
            recent = map(db_article.Article().getArticle,reversedArticle[:11])
        pages,hotArticles = db_article.Article().cutArticlesAsPages(db_article.Article().getHotArticles(),11,1)
        resp = make_response(render_template('index/article.html',article=article,hotArticles=hotArticles,recentRead=recent))
        str_recentRead = '***'.join(map(str,recentRead))
        resp.set_cookie('recentRead',str_recentRead)
        return resp
    else:
        return abort(404)


@app.route('/article/add',methods=['POST','GET'])
@requires_auth
def addArticle():
    if request.method == 'POST':
        title = request.form['title']
        author = session['username']
        article = request.form['article']
        # category = request.form['category']
        if title and author and article:
            db_article.Article().addArticle(0,title,article,author)
            # try:
            #     send_mail([config.Admin],'有人发表了文章','文章作者:{author},文章标题:{title}'.format(author=author,title=title))
            # finally:
            #     return '发表成功'
            return 'success'

        else:
            return '无效的文章'

    else:
        return render_template('user/publish.html')


@app.route('/article/list')
@app.route('/article/list/page/<int:pageNum>')
@requires_auth
def listArticle(pageNum=1):
    allArticles = db_article.Article().getArticleByAuthor(session['username'])
    pages,articles,enum=cutPage(allArticles,20,pageNum)
    return render_template('user/articlelist.html',articles=articles,totalPages=pages,currentPage=pageNum,enum=enum)

@app.route('/article/delete/<articleid>')
@requires_auth
def deleteArticle(articleid):
    db_article.Article().deleteArticle(articleid)

    return redirect('/article/list')
@app.route('/article/update/<articleid>',methods=['GET','POST'])
@requires_auth
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
