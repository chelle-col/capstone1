from flask import Flask, render_template, jsonify, request
import requests as req
from random import randint

app = Flask(__name__)


@app.route("/")
def homepage():
    """Show homepage."""
    # fetch from imgur

    # return homepage

@app.route('/<int:image_id>/edit')
def edit(image_id):
    """Show edit page"""