import functools
from flask import ( Blueprint, flash, g, redirect,
 render_template, request, session, url_for)

from werkzeug.security import check_password_hash, generate_password_hash

from .db import database, User

#
# Any routes that begin with /auth will be sent here 
#

auth = Blueprint("auth", __name__, url_prefix='/auth')



#
# This route will allow users to create an account
# Flashes an error if a field is not complete or username 
# already exists
#

@auth.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Get database
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            # ToDo:
                # Still need to check if in the database before adding
                # add error message
                # Need to set uId to a new number every time
                # Add language 
            user = User(uId=2, username=username, password=password)
            database.session.add(user)
            database.session.commit()


        flash(error)

    return render_template('auth/register.html')




#
# Login page
# Flashes error if username and password do not match
#

@auth.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Get the database
        
        error = None

        # Check username is in the databse
        # if not set error = "Incorrect Username or Password"

        # Check hashed password to matching username
        # if wrong set error = "Incorrect Username or Password"

        # if error is None:
        #   session.clear()
        #   session['user_id'] = USERID FROM DATABASE
        #   return redirect(url_for('index'))
        
        #flash(error)

    return render_template('auth/login.html')




#
# Before anything else is run this will run and check
# if the user is logged in
#
@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        pass
    # get user id from database





@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


#
# This may or may not be used in the future to wrap veiws that
# require a user to be logged in
#
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view