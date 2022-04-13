from flask import (
    Blueprint, render_template, url_for
)

from Telingo.auth import login_required

home = Blueprint("home", __name__)

@home.route('/')
def index():
    return render_template('home/index.html')


@home.route('/profile/<username>')
@login_required
def profile(username):
    if not ('username' in session): #If not logged in, send to login page
        return make_response(redirect(url_for('auth.login')))
    return render_template('home/profile.html')
