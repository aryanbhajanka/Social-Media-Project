#models.py, HobNob

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
 
login = LoginManager()
db = SQLAlchemy()
 
class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'
 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String())
    
 
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
     
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

class PostModel(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String())
    text = db.Column(db.String(100))
    likes = db.Column(db.Integer)

class ProfileModel(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String())
    name = db.Column(db.String())
    bio_account = db.Column(db.String()) 

class FollowModel(db.Model):
    __tablename__ = 'follow'

    id = db.Column(db.Integer, primary_key=True)
    follow_count = db.Column(db.Integer())
    follow_account = db.Column(db.String())
    follower_account = db.Column(db.String())

 
@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))