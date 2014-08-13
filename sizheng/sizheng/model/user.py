__author__ = 'yuan'
from sizheng.model.common import *
from hashlib import md5
class User(Base):
    __tablename__ = 'sizheng_user'
    id = Column(Integer,primary_key=True)
    username = Column(String(20))
    password = Column(String(40))
    state = Column(Integer,default=1) #1:putong 0:admin
    email = Column(String(30))
    phone = Column(Integer,default=0)


    def getUser(self,username):
        user = session.query(User).filter(User.username == username).first()
        if user:
            return user
        else:
            return False

    def getAllUsers(self):
        users = session.query(User)
        return users


    def addUser(self,username,password,email,phone=0):

        user = User(username = username,password = md5(password).hexdigest(),email=email,phone=phone)
        if user:
            session.add(user)
            session.commit()
            return True
        else:
            return False
    def deleteUser(self,id):
        user = session.query(User).filter(User.id == id).first()
        if user:
            session.delete(user)
            session.commit()
            return True
        else:
            return False

    def updateUser(self,id,username,password,state,email,phone=0):
        user = session.query(User).filter(User.id == id)
        if user:
            user.update({"username":username,"password":md5(password).hexdigest(),"state":state,"email":email,"phone":phone})
            session.commit()
            return True
        else:
            return False

    def changePassword(self,username,oldPassword,newPassword):
        if self.confirm(username,oldPassword):
            user = session.query(User).filter(User.username == username)
            user.update({"password":md5(newPassword).hexdigest()})
            session.commit()
            return True
        else:
            return False

    def confirm(self,username,password):
        user = session.query(User).filter(User.username == username).first()
        if user:
            if md5(password).hexdigest() == user.password:
                return True
            else:
                return False

        else:
            return False

    def is_admin(self,username,password):
        if self.confirm(username,password):
            if username == admin_username:
                return True
            else:
                return False
        return False


    def is_exist(self,username):
        user = session.query(User).filter(User.username == username).first()
        if user:
            return True
        else:
            return False
# user = User()
# user.addUser('yuan','950708')