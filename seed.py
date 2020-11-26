from app import db
from models import User, Image, Filter


def seed_db():
    db.drop_all()
    db.create_all()

    db.session.commit()