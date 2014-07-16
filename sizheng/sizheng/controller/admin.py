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

            return redirect('/admin')
        return 'confirm your password'
    else:
        return render_template('userAdd.html')


@app.route('/admin/user/list')
def listUser():
    users = db_user.User().getAllUsers()
    return render_template('userList.html',users=users)

@app.route('/admin/user/update',methods=['POST'])
def updateUser():
    id = request.form['id']
    username = request.form['username']
    password = request.form['password']
    state = request.form['state']
    if id and username and password and state:
        if db_user.User().is_exist(username):
            return 'exist username'
        else:
            db_user.User().updateUser(id,username,password,state)
            return redirect('/admin/user/list')
    else:
        return 'check your input'

@app.route('/admin/user/delete/<userid>')
def deleteUser(userid):
    if db_user.User().deleteUser(userid):
        return redirect('/admin/user/list')
    else:
        return 'there arose a mistake when deleting'

