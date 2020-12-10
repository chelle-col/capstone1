import os
from flask import Flask, flash, render_template, jsonify, request, session, g, redirect
from models import User, Image, Filter, db, connect_db
from forms import UserAddForm, UserLoginForm
import requests as req
from sqlalchemy.exc import IntegrityError
from seed import seed_db
from requests.auth import HTTPBasicAuth
from auth_token import auth_token
from json import loads
from flask_cors import CORS
from classes import Slider, Button

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///capstone1'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

connect_db(app)

CORS(app, resources=r'/image/*')

## Seed database through app. Comment out when not in use
## seed_db()

UNSPLASH_URL = 'https://api.unsplash.com/photos'

## Homepage/Images routes ##

@app.route('/')
def homepage():
    return redirect('/index')

@app.route("/index")
def index():
    """Show homepage."""
    # fetch from unsplash
    resp = req.get(UNSPLASH_URL, params=auth_token)
    prepared = loads(resp.text)
    image_data = [{'url' : item['urls']['thumb'], 'id' : item['id'] }for item in prepared]
    # return homepage
    # TODO add hover effect with javascript
    if not g.user:
        return render_template('display_all.html', image_data=image_data)
    else:
        return render_template('display_all.html', image_data=image_data)

@app.route('/image/<image_id>/edit')
def edit(image_id):
    """Show edit page"""
    sliders = get_sliders()
    buttons = get_buttons()
    resp = req.get(UNSPLASH_URL + '/' + image_id, params=auth_token )
    loaded = loads(resp.text)
    image = {
        'url' : loaded['urls']['small'],
        'width' : loaded['width'],
        'height' : loaded['height']
    }
    return render_template('edit.html', image=image, sliders=sliders, buttons=buttons)

##  Login/Logout/Sign up routes  ###

@app.route('/signup', methods=['Get', 'POST'])
def signup():
    """Show the signup page"""
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")
    return render_template('form.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Show the login page"""
    ## TODO ##
    ## Maybe change/add api login ##
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.authentification(
            username=form.username.data,
            password=form.password.data
            )
        if not user:
            flash('Username/Password is wrong, please try again', 'danger')
            return render_template('form.html', form=form)
        else:
            do_login(user)
            flash('Successfully logged in', 'success')
            return redirect('/')
    else:
        return render_template('form.html', form=form)


@app.route('/logout')
def logout():
    """Log the current user out"""
    do_logout()
    flash('Successfully logged out', 'success')
    return redirect('/')


##  Helper Functions  ##
def do_login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def get_sliders():
    '''Returns a list of sliders with values to use in the html template'''
    #'saturation', 'vibrance', 'contrast', 'exposure', 'hue', 'sepia'
    saturation = Slider('saturation', -100, 100, 0)
    vibrance = Slider('vibrance', -100, 100, 0)
    contrast = Slider('contrast', -5, 5, 0)
    exposure = Slider('exposure', -100, 100, 0)
    hue = Slider('hue', 0, 100, 0)
    sepia = Slider('sepia', 0, 100, 0)
    return [saturation, vibrance, contrast, exposure, hue, sepia]

def get_buttons():
    """Returns a list of buttons with values to use in html template"""
    #'vintage', 'lomo', 'clarity', 'sincity', 'sunrise', 
    #    'crossprocess', 'orangepeel', 'love', 'grungy', 'jarques', 
    #    'pinhole', 'oldboot', 'glowingsun', 'hazydays', 'hermajesty', 
    #    'nostalgia', 'hemingway', 'concentrate'
    vintage = Button('Vintage', 'vintage', 0)
    lomo = Button('Lomo', 'lomo', 1)
    clarity = Button('Clarity', 'clarity', 2)
    sincity = Button('Sin City', 'sincity', 3)
    sunrise = Button('Sunrise', 'sunrise', 4)
    crossprocess = Button('Cross Process', 'crossprocess', 5)
    orangepeel = Button('Orange Peel', 'orangepeel', 6)
    return [ vintage, lomo, clarity, sincity, sunrise, crossprocess, orangepeel]