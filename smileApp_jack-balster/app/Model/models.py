from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# Define the association table postTags
postTags = db.Table('postTags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(1500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)
    happiness_level = db.Column(db.Integer, default = 3)
    
    # Add user_id as a foreign key to associate posts with users
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Define the many-to-many relationship between Post and Tag
    tags = db.relationship('Tag', secondary=postTags, primaryjoin=(postTags.c.post_id == id), backref=db.backref('postTags', lazy='dynamic'), lazy='dynamic')
    
    def get_tags(self):
        return self.tags
    
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return f"Tag(id={self.id}, name='{self.name}')"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Add a back reference to associate users with their posts
    #posts = db.relationship('Post', backref='author', lazy='dynamic')
    posts = db.relationship('Post', backref='writer', lazy='dynamic')

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}')"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_user_posts(self):
        return self.posts
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
