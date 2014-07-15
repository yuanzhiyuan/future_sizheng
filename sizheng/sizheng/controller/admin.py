__author__ = 'yuan'


from flask import *
from sizheng import app
import sizheng.model.article as db_article
import sizheng.model.user as db_user


@app.route('/admin')
def admin():
    return render_template('background.html')

@app.route('/admin/addUser',methods=['POST'])
def addUser():
    username = request.form['username']
    password = request.form['password']
    if db_user.User().is_exist(username):
        return 'exist username'
    else:
        db_user.User().addUser(username,password)

    return redirect('/admin')