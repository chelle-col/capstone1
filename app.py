import os
from flask import Flask, flash, render_template, jsonify, request, session, g, redirect
from models import User, Image, Filter, db, connect_db
from forms import UserAddForm, UserLoginForm
import requests as req
from sqlalchemy.exc import IntegrityError
from seed import seed_db

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///capstone1'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

connect_db(app)

## Seed database through app. Comment out when not in use
## seed_db()

@app.route("/")
def homepage():
    """Show homepage."""
    # fetch from imgur

    # return homepage
    if not g.user:
        return render_template('test.html', title='Home Page Route')
    else:
        return render_template('test.html', title=f'Home Page of {g.user.username}')

@app.route('/<int:image_id>/edit')
def edit(image_id):
    """Show edit page"""

    return render_template('test.html', title='Edit Page Route')


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

###  Login/Logout/Get user ###
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
