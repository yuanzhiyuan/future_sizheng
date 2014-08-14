#encoding=utf8
__author__ = 'yuan'


from flask import *
from sizheng import app
import sizheng.model.article as db_article
import sizheng.model.user as db_user
from sizheng.controller.tools import *
from sizheng.controller.auth import *

@app.route('/admin')
@requires_auth
def admin():
    return render_template('user/background.html')

@app.route('/admin/user/add',methods=['POST','GET'])
@requires_auth
def addUser():
    if request.method == 'POST':
        if request.form['password'] == request.form['repassword']:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            phone = request.form['phone']
            if db_user.User().is_exist(username):
                return 'exist username'
            else:
                db_user.User().addUser(username,password,email,phone)
                try:
                    send_mail([email],'管理员为您注册了用户','用户名是:{musername},密码是:{mpassword},请在{mlogin}上登录'.format(musername=username,mpassword=password,mlogin='sizheng.future.org.cn/login/'))
                finally:
                    return 'add success'

        return '用户名/密码不对'
    else:
        return render_template('admin/userAdd.html')


@app.route('/admin/user/list')
@requires_auth
def listUser():
    users = db_user.User().getAllUsers()
    return render_template('admin/userList.html',users=users)

@app.route('/admin/user/update',methods=['POST'])
@requires_auth
def updateUser():
    #userid is str
    userid = request.form['id']
    username = request.form['username']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']
    state = request.form['state']
    if userid and username and password and state and email:
        user = db_user.User().getUser(username)
        if user:
            if user.id == int(userid):
                db_user.User().updateUser(userid,username,password,state,email,phone)

                return '更新成功'
            else:
                return '用户名已存在'

        else:
            db_user.User().updateUser(userid,username,password,state,email,phone)
            return '更新成功'
    else:
        return '检查你的输入'

@app.route('/admin/user/delete/<userid>')
@requires_auth
def deleteUser(userid):
    if db_user.User().deleteUser(userid):
        return redirect('/admin/user/list')
    else:
        return '删除时出现错误'


@app.route('/admin/article/verify',methods=['GET','POST'])
@app.route('/admin/article/verify/page/<int:pageNum>',methods=['GET','POST'])
@requires_auth
def verify(pageNum=1):
    if request.method == 'GET':

        allArticles = db_article.Article().getUnverifiedArticles()
        pages,articles,enum=cutPage(allArticles,20,pageNum)
        return render_template('admin/admin_articleVerify.html',articles=articles,totalPages=pages,currentPage=pageNum,enum=enum)


    elif request.method == 'POST':
        email = db_user.User().getUser(session['username']).email
        articleid = request.form['articleid']
        article = db_article.Article().getArticle(int(articleid))
        if request.form['type'] == 'pass':
            db_article.Article().verify(int(articleid))
            try:
                send_mail([email],'您的文章已通过管理员审核','文章标题:{title},文章id:{id}'.format(title=article.title,id=articleid))
            finally:
                return '通过成功'
        elif request.form['type'] == 'unpass':
            db_article.Article().deleteArticle(int(request.form['articleid']))
            try:
                send_mail([email],'您的文章未通过管理员审核','文章标题:{title},文章id:{id}'.format(title=article.title,id=articleid))
            finally:
                return '不通过成功'
        else:
            return '审核出现错误'

@app.route('/admin/article/list')
@app.route('/admin/article/list/page/<int:pageNum>')
@requires_auth
def admin_listAllArticles(pageNum=1):
    allArticles = db_article.Article().getAllArticles()
    pages,articles,enum=cutPage(allArticles,20,pageNum)
    return render_template('admin/admin_articleList.html',articles=articles,totalPages=pages,currentPage=pageNum,enum=enum)



@app.route('/admin/article/delete',methods=['POST'])
@requires_auth
def admin_deleteArticle():
    articleid = request.form['articleid']
    if db_article.Article().deleteArticle(articleid):
        return '删除成功'
    else:
        return '删除失败'

@app.route('/admin/article/verified')
@app.route('/admin/article/verified/page/<int:pageNum>')
@requires_auth
def listVerified(pageNum=1):
    allArticles = db_article.Article().getVerifiedArticles()
    pages,articles,enum=cutPage(allArticles,20,pageNum)
    return render_template('admin/verifiedArticle.html',articles=articles,totalPages=pages,currentPage=pageNum,enum=enum)

