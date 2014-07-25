#encoding=utf8
__author__ = 'yuan'


from flask import *
from sizheng import app
import sizheng.model.article as db_article
import sizheng.model.user as db_user
from sizheng.controller.tools import *

@app.route('/admin')
def admin():
    return render_template('user/background.html')

@app.route('/admin/user/add',methods=['POST','GET'])
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
                send_mail([email],'管理员为您注册了用户','用户名是:{musername},密码是:{mpassword},请在{mlogin}上登录'.format(musername=username,mpassword=password,mlogin='sizheng.future.org.cn/login/'))
                return 'add success'

        return 'confirm your password'
    else:
        return render_template('admin/userAdd.html')


@app.route('/admin/user/list')
def listUser():
    users = db_user.User().getAllUsers()
    return render_template('admin/userList.html',users=users)

@app.route('/admin/user/update',methods=['POST'])
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

                return 'success'
            else:
                return 'exist username'

        else:
            db_user.User().updateUser(userid,username,password,state,email,phone)
            return 'success'
    else:
        return 'check your input'

@app.route('/admin/user/delete/<userid>')
def deleteUser(userid):
    if db_user.User().deleteUser(userid):
        return redirect('/admin/user/list')
    else:
        return 'there arose a mistake when deleting'


@app.route('/admin/article/verify',methods=['GET','POST'])
def verify():
    if request.method == 'GET':

        articles = db_article.Article().getUnverifiedArticles()
        return render_template('admin/admin_articleVerify.html',articles=articles)
    elif request.method == 'POST':
        email = db_user.User().getUser(session['username']).email
        articleid = request.form['articleid']
        article = db_article.Article().getArticle(int(articleid))
        if request.form['type'] == 'pass':
            db_article.Article().verify(int(articleid))
            send_mail([email],'您的文章已通过管理员审核','文章标题:{title},文章id:{id}'.format(title=article.title,id=articleid))
            return 'pass success'
        elif request.form['type'] == 'unpass':
            db_article.Article().deleteArticle(int(request.form['articleid']))
            send_mail([email],'您的文章未通过管理员审核','文章标题:{title},文章id:{id}'.format(title=article.title,id=articleid))
            return 'unpass success'
        else:
            return 'error'

@app.route('/admin/article/list')
def admin_listAllArticles():
    articles = db_article.Article().getAllArticles()
    return render_template('admin/admin_articleList.html',articles=articles)

@app.route('/admin/article/delete',methods=['POST'])
def admin_deleteArticle():
    articleid = request.form['articleid']
    if db_article.Article().deleteArticle(articleid):
        return 'delete success'
    else:
        return 'delete failed'