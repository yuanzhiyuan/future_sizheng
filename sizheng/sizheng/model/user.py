__author__ = 'yuan'
from sizheng.model.common import *
class User(Base):
    __tablename__ = 'sizheng_user'
    id = Column(Integer,primary_key=True)
    username = Column(String(20))
    password = Column(String(20))
    state = Column(Integer,default=1) #1:putong 0:admin

    def addUser(self,username,password):
        current_user = session.query(User).order_by(desc(User.id)).first()
        if current_user:
            theid = current_user.id+1
        else:
            theid = 0
        user = User(id = theid,username = username,password = password)
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

    def changePassword(self,username,oldPassword,newPassword):
        if self.confirm(username,oldPassword):
            user = session.query(User).filter(User.username == username).first()
            user.update({"password":newPassword})
            session.commit()
            return True
        else:
            return False

    def confirm(self,username,password):
        user = session.query(User).filter(User.username == username).first()
        if user:
            if password == user.password:
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