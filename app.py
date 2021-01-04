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
from flask_cors import cross_origin
from classes import Slider, Button
from base64 import b64decode, b64encode
from PIL import Image as img
from io import BytesIO

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///capstone1'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

connect_db(app)

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
    resp = req.get(UNSPLASH_URL, params={'client_id' : auth_token, 'per_page': '20'})
    prepared = loads(resp.text)
    image_data = [{'url' : item['urls']['thumb'], 'id' : item['id'] }for item in prepared]
    # return homepage
    if not g.user:
        return render_template('display_all.html', image_data=image_data)
    else:
        return render_template('display_all.html', image_data=image_data)

@app.route('/image/<image_id>/new', methods=['GET'])
@cross_origin()
def new(image_id):
    """Show new edit page, and to put a filter on images that don't have one yet"""
    # Future stuff When coming from upload page two images are saved in db - change to one
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
    
    sliders = get_sliders()
    buttons = get_buttons()
    user_filters = g.user.user_filters
    whole_image = Image.query.get(image_id)
    # If it has a unsplash id then it comes from there - use it
    if not whole_image.unsplash_id:
        unsplash_id = whole_image.unsplash_id 
        resp = req.get(UNSPLASH_URL + '/' + unsplash_id, params={'client_id': auth_token} )
        loaded = loads(resp.text)
        image = {
            'url' : loaded['urls']['small'],
            'width' : 400,
            'height' : loaded['height']*(400/loaded['width']),
            'unsplash' : image_id
        }
        return render_template('edit.html', image=image, 
                                sliders=sliders, buttons=buttons, 
                                user_filters=user_filters)
    # Else is for images in our db/new images
    else:
        return render_template('edit.html', image=whole_image, 
                                sliders=sliders, buttons=buttons, 
                                user_filters=user_filters)

@app.route('/image/<image_id>/edit', methods=['GET'])
@cross_origin()
def edit(image_id):
    """Edit current images that a user has"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    sliders = get_sliders()
    buttons = get_buttons()
    user_filters = g.user.user_filters
    image = Image.query.get_or_404(image_id)
    filter_id = image.filter.id
    # if an image url starts with data tag it is from db
    # Future note: Change to look like new route
    if image.url[:4] == 'data':
        return render_template('edit.html',  image=image, 
                            sliders=sliders, buttons=buttons, 
                            user_filters=user_filters, filter_id=filter_id)
    resp = req.get(UNSPLASH_URL + '/' + image.unsplash_id, params={'client_id': auth_token} )
    loaded = loads(resp.text)
    image = {
        'url' : loaded['urls']['small'],
        'width' : 400, 
        'height' : loaded['height']*(400/loaded['width'])
    }
    return render_template('edit.html',  image=image, 
                            sliders=sliders, buttons=buttons, 
                            user_filters=user_filters, filter_id=filter_id)

@app.route('/image/upload')
def upload():
    """Display the page for uploading an image to our db"""
    return render_template('upload.html')

@app.route('/my_filters')
def show_my_filters():
    """Display all of a users filters on a single image"""
    filters = g.user.user_filters
    return render_template('list_filters.html', filters=filters)

@app.route('/my_pictures')
@cross_origin()
def show_my_pictures():
    """Display all of a users picture with the filters on them"""
    pictures = g.user.pics
    return render_template('list_pictures.html', pictures=pictures)

@app.route('/my_profile')
def show_my_profile():
    """Displays profile page"""
    # Not fully implmented. Left for future me
    return render_template('title.html', title='Profile root left in to show how to expand this app.')

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
# I know the names are wrong. Will Fix soon
# TODO add routes to give different sized images
#'/api/filter/new'
@app.route('/api/save_filter', methods=['POST'])
@cross_origin()
def save_filter():
    """Adds filter to db and returns the new filter"""
    data = request.get_json()['data']
    load_data = loads(data)
    user =  User.query.get(load_data['id'])
    new_filter = add_filter_2_db(name=load_data['name'], ranges=load_data['ranges'], user=user)

    if len(load_data['presets']) > 0:
        add_presets_2_filter(new_filter=new_filter, presets=load_data['presets'])

    #  TODO add error for blank name
    return new_filter.serialize()

#'/api/image/filter/new'
@app.route('/api/save_pic_filter', methods=['POST'])
@cross_origin()
def save_pic_filter():
    """Adds filter and image to db and returns the new filter"""
    data = request.get_json()['data']
    load_data = loads(data)
    user =  User.query.get(load_data['id'])
    new_filter = add_filter_2_db(name=load_data['name'], ranges=load_data['ranges'], user=user)

    add_presets_2_filter(new_filter=new_filter, presets=load_data['presets'])
    new_image = Image(url=load_data['image'], user_id=user.id, filter_id=new_filter.id, unsplash_id=load_data['unsplash_id'])
    db.session.add_all([new_filter, new_image])
    db.session.commit()
    return new_image.serialize()

@app.route('/api/filter/<int:filter_id>', methods=['GET'])
@cross_origin()
def get_filter(filter_id):
    """Returns the requested filter"""
    filter = Filter.query.get_or_404(filter_id)
    columns = Filter.__table__.columns.keys()
    sliders = columns[3:]
    return {
        'name' : filter.full_name,
        'ranges' : {slider:getattr(filter, slider) for slider in sliders},
        'presets' : [preset.id for preset in filter.preset_filters]
    }
#'/api/filter/<id>/delete'
@app.route('/api/remove_filter', methods=['POST'])
@cross_origin()
def remove_filter():
    """Removes the filter from db"""
    data = request.get_json()['data']
    load_data = loads(data)
    user =  User.query.get(load_data['id'])
    filter = Filter.query.get(load_data['filter_id'])
    user.user_filters.remove(filter)
    db.session.delete(filter)
    db.session.commit()
    return 'deleted'
#'api/image/<id>/delete
@app.route('/api/remove_picture', methods=['POST'])
@cross_origin()
def remove_picture():
    """Removes the picture and all filter data from db"""
    data = request.get_json()['data']
    load_data = loads(data)
    user =  User.query.get(load_data['id'])
    picture = Image.query.get(load_data['filter_id'])
    user.pics.remove(picture)
    db.session.delete(picture)
    db.session.commit()
    return 'deleted'
# api/image/upload
@app.route('/api/upload_picture', methods=['POST'])
@cross_origin()
def upload_picture():
    """Adds the base64 representation of the image to the db"""
    data = request.get_json()['data']
    load_data = loads(data)
    user =  User.query.get(load_data['id'])
    converted_image = convert_image(load_data['image'])
    image = Image(user_id=user.id, url=converted_image['url'], 
                    width=converted_image['width'], height=converted_image['height'])
    db.session.add(image)
    db.session.commit()
    return jsonify(image.id)
# '/api/filter/<id>/update'
@app.route('/api/update_filter', methods=['POST'])
@cross_origin()
def update_filter():
    """Updates the filter in the db and returns the filter"""
    data = request.get_json()['data']
    load_data = loads(data)
    Filter.query.filter_by(id=load_data['filter_id']).update(load_data['ranges'])
    db.session.commit()
    filter = Filter.query.get(load_data['filter_id'])
    return filter.serialize()

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
    noise = Slider('noise', 0, 100, 0)
    return [saturation, vibrance, contrast, exposure, hue, sepia, noise]

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
    love = Button('Love', 'love', 8)
    grungy = Button('Grungy', 'grungy', 9)
    jarques = Button('Jarques', 'jarques', 10)
    pinhole = Button('Pinhole', 'pinhole', 11)
    oldboot = Button('Old Boot', 'oldboot', 12)
    glowingsun = Button('Glowing Sun', 'glowingsun', 13)
    hazydays = Button('Hazy Days', 'hazydays', 14)
    hermajesty = Button('Her Majesty', 'hermajesty', 15)
    nostalgia = Button('Nostalgia', 'nostalgia', 16)
    hemingway = Button('Hemingway', 'hemingway', 17)
    concentrate = Button('Concentrate', 'concentrate', 18)
    return [ vintage, lomo, clarity, sincity, sunrise, crossprocess, orangepeel, love,
                grungy, jarques, pinhole, oldboot, glowingsun, hazydays, hermajesty,
                nostalgia, hemingway, concentrate]

def add_presets_2_filter(new_filter, presets):
    """Takes an array and places them on the filter"""
    for id in presets:
        filter = Filter.query.get(id)
        new_filter.preset_filters.append(filter)
    db.session.commit()

def add_filter_2_db(name, ranges, user):
    """Adds the new filter to the db"""
    new_filter = Filter(
        # Choose not to use a for loop for optimization
        # Still really slow though
        user_id=user.id,
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

def convert_image(raw_im):
    """Resizes and readies the image before it's put into db"""
    # Strip the html data from the image so we can use it in pillow
    image_bytes = raw_im.replace('data:image/png;base64,', '')
    # Open the image into Pillow
    im = img.open(BytesIO(b64decode(image_bytes)))
    # Resize
    resized_im = im.resize((350, round(im.size[1]*350/im.size[0])))
    # Buffer so we can read out again
    buffered = BytesIO()
    # Save resized image
    resized_im.save(buffered, format="PNG")
    # Encode again in base64
    im_encode = b64encode(buffered.getvalue())
    # This turns into a string ready for db
    im_data = im_encode.decode()
    new_image = {
        'width' : resized_im.size[0],
        'height' : resized_im.size[1],
        'url' : "data:image/png;base64," + im_data
    }
    return new_image