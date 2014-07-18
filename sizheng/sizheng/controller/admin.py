__author__ = 'yuan'


from flask import *
from sizheng import app
import sizheng.model.article as db_article
import sizheng.model.user as db_user


@app.route('/admin')
def admin():
    return render_template('background.html')

@app.route('/admin/user/add',methods=['POST','GET'])
def addUser():
    if request.method == 'POST':
        if request.form['password'] == request.form['repassword']:
            username = request.form['username']
            password = request.form['password']
            if db_user.User().is_exist(username):
                return 'exist username'
            else:
                db_user.User().addUser(username,password)
                return 'add success'

        return 'confirm your password'
    else:
        return render_template('userAdd.html')


@app.route('/admin/user/list')
def listUser():
    users = db_user.User().getAllUsers()
    return render_template('userList.html',users=users)

@app.route('/admin/user/update',methods=['POST'])
def updateUser():
    #userid is str
    userid = request.form['id']
    username = request.form['username']
    password = request.form['password']
    state = request.form['state']
    if userid and username and password and state:
        user = db_user.User().getUser(username)
        if user:
            if user.id == int(userid):
                db_user.User().updateUser(userid,username,password,state)
                return 'success'
            else:
                return 'exist username'

        else:
            db_user.User().updateUser(userid,username,password,state)
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
        return render_template('admin_articleVerify.html',articles=articles)
    elif request.method == 'POST':
        if request.form['type'] == 'pass':
            db_article.Article().verify(int(request.form['articleid']))
            return 'pass success'
        elif request.form['type'] == 'unpass':
            db_article.Article().deleteArticle(int(request.form['articleid']))
            return 'unpass success'
        else:
            return 'error'

@app.route('/admin/article/list')
def admin_listAllArticles():
    articles = db_article.Article().getAllArticles()
    return render_template('admin_articleList.html',articles=articles)

@app.route('/admin/article/delete',methods=['POST'])
def admin_deleteArticle():
    articleid = request.form['articleid']
    if db_article.Article().deleteArticle(articleid):
        return 'delete success'
    else:
        return 'delete failed'