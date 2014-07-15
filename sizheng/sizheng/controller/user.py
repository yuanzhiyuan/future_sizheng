__author__ = 'yuan'
from flask import *
from sizheng import app

import sizheng.model.article as db_article
import sizheng.model.user as db_user

@app.route('/login/',methods=['GET','POST'])
def login():

    if request.method == 'POST':
        if db_user.User().confirm(request.form['username'],request.form['password']):
            session['username'] = request.form['username']
            session['password'] = request.form['password']

            if db_user.User().is_admin(request.form['username'],request.form['password']):
                return redirect('/admin')
            else:
                return redirect('/user/'+request.form['username'])
        else:
            return 'check your username and password!'
    if request.method == 'GET':
        return render_template('login.html')


@app.route('/user/<username>')
def user(username):
    return render_template('publish.html',username=username)

