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
            user = db_user.User().getUser(request.form['username'])
            session['state'] = user.state

            if session['state'] == 0:
                return redirect('/admin')
            else:
                return redirect('/user/'+request.form['username'])
        else:
            return 'check your username and password!'
    if request.method == 'GET':
        return render_template('login.html')


@app.route('/user/<username>')
def user(username):
    return render_template('background.html',username=username)



@app.route('/logout')
def logout():
    session.pop('username',None)
    session.pop('password',None)
    session.pop('state',None)
    return redirect('/')


@app.route('/user/changePassword',methods=['GET','POST'])
def changePassword():
    if request.method == 'GET':
        return render_template('changePassword.html')
    elif request.method == 'POST':
        if db_user.User().confirm(session['username'],request.form['oldpassword']):
            if request.form['newpassword'] == request.form['repassword']:
                db_user.User().changePassword(session['username'],request.form['oldpassword'],request.form['repassword'])
                if session['state'] == 0:
                    return redirect('/admin')
                else:
                    return redirect('/user/'+session['username'])
            else:
                return 'old and new password does not match'
        else:
            return 'wrong password'

