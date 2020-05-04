from webapp import db,login_manger
from flask_login import UserMixin
import time
from datetime import datetime
@login_manger.user_loader
def load_user(user_id):
    return Chatusers.query.get(int(user_id))

class Chatusers(UserMixin,db.Model):
    __tablename__="chatusers"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30) , unique=True,nullable=False)
    email =db.Column(db.String(30) , unique=True,nullable=False)
    password = db.Column(db.String(100),unique=True,nullable=False)

    def __init__(self,username,email,password):
        self.username=username
        self.email=email
        self.image=None
        self.password=password

    def __repr__(self):
        return f'username {self.username},{self.email}'
    def serialize(self):
        return {"id":self.id,
                "username":self.username,
                "password":self.password,
                "email":self.email}

class Post(UserMixin,db.Model):
    __tablename__ = "post"
    id=db.Column(db.Integer,primary_key=True)
    date_posted= db.Column(db.String ,nullable=False,default= (time.strftime('%b-%d %I:%M%p', time.localtime())))
    content = db.Column(db.String(100), nullable=True)
    room =db.Column(db.String(10),nullable=False)



    def __repr__(self):
        return f'time {self.date_posted} content{self.content}'
    def serialize(self):
        return {"id":self.id,
                "time":self.date_posted,
                "msg":self.content,
                'room':self.room}


