from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Store the user information, and provide sign up and authentification"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)
    bio = db.Column(db.Text)

    @classmethod
    def signup(cls):
        return

    @classmethod
    def authentification(cls):
        return

class Image(db.Model):
    """Store the image information"""
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Coulmn(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Filter(db.Model):
    """Store the name and data of custom & default filters"""
    __tablename__ = 'filters'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.Text, nullable=false)
    user_id = db.Column(db.Text, db.ForeignKey('users.id'))
    brightness = db.Column(db.Text)
    contrast = db.Column(db.Text)
    saturation = db.Column(db.Text)

class ImageFilter(db.Model):
    """Connection of images and filters"""

    __tablename__ = 'image_filters'

    image_id = db.Column(
        db.Integer,
        db.ForeignKey('images.id', ondelete="cascade"),
        primary_key=True,
    )

    filter_id = db.Column(
        db.Integer,
        db.ForeignKey('filters.id', ondelete="cascade"),
        primary_key=True,
    )