from email.policy import default
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, delete, desc,   func


#initialize sqlAlchemy

db =SQLAlchemy()
#connect app to db instance
def connectdb(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User table creation"""
    __tablename__ ='users'

    id= db.Column(db.Integer, primary_key = True, autoincrement =True)    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(250))

    @classmethod
    def delete_user(cls, user_id):
        User.query.filter_by(id =user_id).delete()
        db.session.commit()

class Tag(db.Model):
    """Tag table creation"""
    __tablename__ ='tags'

    id= db.Column(db.Integer, primary_key = True, autoincrement =True)    
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    @classmethod
    def recent_tags(cls):
        tag = Tag.query.order_by(desc(Tag.name)).limit(5)
        return tag

    @classmethod
    def add_new_tag(cls, name):
        new_tag = Tag(name = name)
        db.session.add(new_tag)
        db.session.commit()         
    @classmethod
    def detail_tag(cls, tag_id):
        return Tag.query.filter_by(id =tag_id).first()

class Post(db.Model):
    """Post table creation"""
    __tablename__ ='posts'

    id= db.Column(db.Integer, primary_key = True, autoincrement =True)    
    title = db.Column(db.String(50), nullable=False, unique=True)
    content = db.Column(db.String(300), nullable=False)
    created_at  = db.Column(db.DateTime, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  
    usr = db.relationship('User', backref='posts')
    postTags = db.relationship('Tag', secondary='posts_tags', backref='posts')
    

    @classmethod
    def get_post_all(cls, user_id):
        return Post.query.filter_by(user_id =user_id).all()

    @classmethod
    def detail_post(cls, post_id):
        return Post.query.filter_by(id =post_id).first()
 
    @classmethod
    def delete_post(cls, post_id):
        Post.query.filter_by(id =post_id).delete()
        db.session.commit()
    @classmethod
    def add_new_post(cls, title, content,user_id):
        new_post = Post(title = title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit() 


    @classmethod
    def edit_post(cls, post_id,title, content):
        post = Post.query.get_or_404(post_id)
        post.title = title
        post.content = content
        post.created_at = func.now()
        db.session.add(post)
        db.session.commit()



    @classmethod
    def recent_post(cls):
        post = Post.query.order_by(desc(Post.created_at)).limit(5)
        return post


     
class PostTag(db.Model):
    """PostTag table creation"""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer,
                       db.ForeignKey("posts.id"),
                       primary_key=True)
    tag_id = db.Column(db.Integer,
                          db.ForeignKey("tags.id"),
                          primary_key=True)    