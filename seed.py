from app import db
from models import User, Image, Filter


def seed_db():
    db.drop_all()
    db.create_all()

    bla = User.signup(username='bla', password='blablabla', email='bla@bla.com', image_url='')

    vintage = Filter(full_name='vintage')
    lomo = Filter(full_name='lomo')
    clarity = Filter(full_name='clarity')
    sincity = Filter(full_name='sincity')
    sunrise = Filter(full_name='sunrise')
    crossprocess = Filter(full_name='crossprocess')
    orangepeel = Filter(full_name='orangepeel')

    db.session.add_all([vintage, lomo, clarity, sincity, sunrise, crossprocess, orangepeel])
    db.session.commit()