from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

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
    image_url = db.Column(db.Text)

    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user. Hashes password and adds user to system."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(
            username=username,
            email=email,
            password_hash=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authentification(cls, username, password):
        """If username and password checks out then return user else return false"""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password_hash, password)
            if is_auth:
                return user

        return False

class Image(db.Model):
    """Store the image information"""
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Filter(db.Model):
    """Store the name and data of custom & default filters"""
    __tablename__ = 'filters'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
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