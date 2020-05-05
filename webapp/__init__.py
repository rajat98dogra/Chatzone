from flask import Flask, render_template, request ,flash
from flask_sqlalchemy import  SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =os.environ.get('DATABASE_URL')
    # 'postgresql://postgres:root@localhost/chat'
app.secret_key= os.environ.get('SECRET_KEY')


socketio = SocketIO(app)
db =SQLAlchemy(app)
login_manger=LoginManager(app)
login_manger.login_view='login'
login_manger.login_message_category='info'


from webapp import routes