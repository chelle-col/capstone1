import os
from flask import Flask, flash, render_template, jsonify, request, session, g, redirect, send_from_directory
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
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

connect_db(app)

CORS(app, resources=r'/image/*')

## Seed database through app. Comment out when not in use
# seed_db()

UNSPLASH_URL = 'https://api.unsplash.com/photos'

## Homepage/Images routes ##

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

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
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
    
    sliders = get_sliders()
    buttons = get_buttons()
    user_filters = g.user.user_filters
    resp = req.get(UNSPLASH_URL + '/' + image_id, params=auth_token )
    loaded = loads(resp.text)
    image = {
        'url' : loaded['urls']['small'],
        'width' : loaded['width'],
        'height' : loaded['height']
    }
    return render_template('edit.html', image=image, sliders=sliders, buttons=buttons, user_filters=user_filters)

@app.route('/my_filters')
def show_my_filters():
    filters = g.user.user_filters
    return render_template('list_filters.html', title='Edit Filters Route', filters=filters)

@app.route('/my_pictures')
def show_my_pictures():
    pictures = g.user.pics
    return render_template('list_pictures.html', pictures=pictures)

@app.route('/my_profile')
def show_my_profile():
    return render_template('test.html', title='Edit Profile Route')

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

### API Routes ###
@app.route('/api/save_filter', methods=['POST'])
def save_filter():
    data = request.get_json()['data']
    load_data = loads(data)
    new_filter = add_filter_2_db(name=load_data['name'], ranges=load_data['ranges'])

    if len(load_data['presets']) > 0:
        add_presets_2_filter(new_filter=new_filter, presets=load_data['presets'])

    #  TODO add error for blank name
    return new_filter.serialize()

def add_presets_2_filter(new_filter, presets):
    for id in presets:
        filter = Filter.query.get(id)
        new_filter.preset_filters.append(filter)
    db.session.commit()

def add_filter_2_db(name, ranges):
    new_filter = Filter(
        user_id=g.user.id,
        full_name=name,
        saturation=ranges['saturation'],
        vibrance=ranges['vibrance'],
        contrast=ranges['contrast'],
        exposure=ranges['exposure'],
        hue=ranges['hue'],
        sepia=ranges['sepia']
    )
    db.session.add(new_filter)
    db.session.commit()
    return new_filter

@app.route('/api/save_pic_filter', methods=['POST'])
def save_pic_filter():
    data = request.get_json()['data']
    load_data = loads(data)
    new_filter = add_filter_2_db(name=load_data['name'], ranges=load_data['ranges'])
    add_presets_2_filter(new_filter=new_filter, presets=load_data['presets'])
    new_image = Image(url=load_data['image'], user_id=g.user.id, filter_id=new_filter.id)
    db.session.add_all([new_filter, new_image])
    db.session.commit()
    return new_image.serialize()

@app.route('/api/filter/<int:filter_id>', methods=['GET'])
def get_filter(filter_id):
    filter = Filter.query.get_or_404(filter_id)
    columns = Filter.__table__.columns.keys()
    sliders = columns[3:]
    return {
        'name' : filter.full_name,
        'ranges' : {slider:getattr(filter, slider) for slider in sliders},
        'presets' : [preset.id for preset in filter.preset_filters]
    }

@app.route('/api/remove_filter', methods=['POST'])
def remove_filter():
    data = request.get_json()['data']
    load_data = int(loads(data))
    filter = Filter.query.get(load_data)
    g.user.user_filters.remove(filter)
    db.session.delete(filter)
    db.session.commit()
    return f'deleted'


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
    contrast = Slider('contrast', -20, 20, 0)
    exposure = Slider('exposure', -100, 100, 0)
    hue = Slider('hue', 0, 100, 0)
    sepia = Slider('sepia', 0, 100, 0)
    # Add more here, remember to add to edit.js too
    return [saturation, vibrance, contrast, exposure, hue, sepia]

def get_buttons():
    """Returns a list of buttons with values to use in html template"""
    #'vintage', 'lomo', 'clarity', 'sincity', 'sunrise', 
    #    'crossprocess', 'orangepeel', 'love', 'grungy', 'jarques', 
    #    'pinhole', 'oldboot', 'glowingsun', 'hazydays', 'hermajesty', 
    #    'nostalgia', 'hemingway', 'concentrate'
    vintage = Button('Vintage', 'vintage', 1)
    lomo = Button('Lomo', 'lomo', 2)
    clarity = Button('Clarity', 'clarity', 3)
    sincity = Button('Sin City', 'sincity', 4)
    sunrise = Button('Sunrise', 'sunrise', 5)
    crossprocess = Button('Cross Process', 'crossprocess', 6)
    orangepeel = Button('Orange Peel', 'orangepeel', 7)
    return [ vintage, lomo, clarity, sincity, sunrise, crossprocess, orangepeel]