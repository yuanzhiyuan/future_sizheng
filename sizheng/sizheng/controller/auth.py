#encoding:utf8
__author__ = 'yuan'
from functools import wraps
from flask import url_for,redirect,session,request

admin_auth=['addUser',
            'listUser',
            'updateUser',
            'deleteUser',
            'verify',
            'admin_listAllArticles',
            'admin_deleteArticle',
            'listVerified']

def requires_auth(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'username' and 'state' in session:
            #@DEBUG print '/'.join(request.url.split('/')[3:])
            if f.__name__ in admin_auth:
                if session['state'] == 0:
                    return f(*args, **kwargs)
                else:
                    return '您没有权限执行此操作!'
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapped