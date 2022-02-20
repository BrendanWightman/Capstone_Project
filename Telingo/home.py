from flask import (
    Blueprint, render_template
)

from Telingo.auth import login_required

home = Blueprint("home", __name__)

@home.route('/')
def index():
    return render_template('home/index.html')


@home.route('/profile/<username>')
@login_required
def profile(username):
    return render_template('home/profile.html')