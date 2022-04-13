from flask import (
    Blueprint, render_template, url_for, session, request
)

from Telingo.auth import login_required
from .db import Admin, Language, database, User

home = Blueprint("home", __name__)

@home.route('/')
def index():
    return render_template('home/index.html')


@home.route('/profile/<username>')
#@login_required
def profile(username):
    if not ('username' in session): #If not logged in, send to login page
        return make_response(redirect(url_for('auth.login')))

    user = User.query.filter_by(username = username).first()
    return render_template('home/profile.html', user=user)

@home.route('/profile/<username>/edit', methods=('GET', 'POST'))
def edit(username):
    if not ('username' in session): #If not logged in, send to login page
        return make_response(redirect(url_for('auth.login')))

    user = User.query.filter_by(username = username).first()
    if request.method == 'POST':
        #Get form elements
        new_native_lang = request.form['new_native_lang']
        new_language = request.form['edit_language']
        proficiency = int(request.form['language_proficiency'])

        record = Language.query.with_parent(user).filter(Language.language == new_language).first()
        if record: #If language already exists, just update proficiency
            record.fluency = proficiency
        else: #Otherwise, add new language
            new_language_elem = Language(language=new_language, fluency=proficiency)
            user.languages.append(new_language_elem)
        #Commit and redirect
        user.native_lang = new_native_lang
        database.session.commit()
        return render_template('home/profile.html',user=user)
    return render_template('home/profile_edit.html',user=user)
