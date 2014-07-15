from sizheng import config

__author__ = 'yuan'
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('mysql://{}:{}@localhost:3306/{}?charset=utf8'.format(config.DB_USERNAME, config.DB_PASSWORD,
                                                                             config.DB_DB),pool_recycle=7200,encoding = 'utf-8', echo=False)
Session = sessionmaker(bind = engine)
session = Session()
Base = declarative_base()

admin_username = 'admin'
admin_password = 'hehe'