__author__ = 'yuan'


from flask import *
from sizheng import config
app = Flask(__name__)
app.secret_key = 'fuck'
import sizheng.controller.index
import sizheng.controller.article
import sizheng.controller.user
import sizheng.controller.admin
import sizheng.controller.tools
import sizheng.controller.test
import sizheng.controller.errorHandler


