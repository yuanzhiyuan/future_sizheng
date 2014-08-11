#encoding=utf8
__author__ = 'yuan'
from flask import *
from sizheng import app

import sizheng.model.article as db_article
import sizheng.model.user as db_user
from sizheng.controller.auth import *

@app.route('/login/',methods=['GET','POST'])
def login():

    if request.method == 'POST':
        if db_user.User().confirm(request.form['username'],request.form['password']):
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            user = db_user.User().getUser(request.form['username'])
            session['state'] = user.state

            if session['state'] == 0:
                return 'admin'
                # return redirect('/admin')
            else:
                return 'user'
                # return redirect('/user/'+request.form['username'])
        else:
            return 'check your username and password!'
    if request.method == 'GET':
        return render_template('user/login.html')


@app.route('/user/<username>')
@requires_auth
def user(username):
    return render_template('user/background.html',username=username)



@app.route('/logout')
def logout():
    session.pop('username',None)
    session.pop('password',None)
    session.pop('state',None)
    return redirect('/')


@app.route('/user/changePassword',methods=['GET','POST'])
@requires_auth
def changePassword():
    if request.method == 'GET':
        return render_template('user/changePassword.html')
    elif request.method == 'POST':
        if db_user.User().confirm(session['username'],request.form['oldpassword']):
            if request.form['newpassword'] == request.form['repassword']:
                db_user.User().changePassword(session['username'],request.form['oldpassword'],request.form['repassword'])
                return 'success'
            else:
                return '两次密码不一致'
        else:
            return '密码错误'


@app.route('/user/frame/<position>')
@requires_auth
def showFrame(position):
    if position == 'left':
        return render_template('user/frame_left.html')
    if position == 'right':
        return render_template('user/frame_right.html')
    else:
        return False

@app.route('/user/shouldKnow')
@requires_auth
def shouldKnow():
    return render_template('user/frame_right.html')