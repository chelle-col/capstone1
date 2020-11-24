import os
from flask import Flask, render_template, jsonify, request
from models import User, Image, Filter, db, connect_db
from forms import UserAddForm
import requests as req

app = Flask(__name__)

connect_db(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

@app.route("/")
def homepage():
    """Show homepage."""
    # fetch from imgur

    # return homepage
    return render_template('test.html', title='Home Page Route')

@app.route('/<int:image_id>/edit')
def edit(image_id):
    """Show edit page"""

    return render_template('test.html', title='Edit Page Route')


@app.route('/signup')
def signup():
    """Show the signup page"""
    form = UserAddForm()

    return render_template('form.html', form=form)

@app.route('/login')
def login():
    """Show the login page"""
    return render_template('test.html', title='Login Route')


@app.route('/logout', methods=['POST'])
def logout():
    """Log the current user out"""
    return render_template('test.html', title='Logout Route')


