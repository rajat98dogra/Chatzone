from webapp.models import db
from flask import  Flask
app=Flask(__name__)
import  os
app.config['SQLALCHEMY_DATABASE_URI'] =os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)

def main():
    db.create_all()
if __name__ == '__main__':
    with app.app_context():
        main()
