from calendar import day_abbr
import functools
from multiprocessing.reduction import duplicate
from flask import ( Blueprint, flash, g, redirect,
 render_template, request, session, url_for)

from werkzeug.security import check_password_hash, generate_password_hash

from .db import Language, database, User

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
        new_username = request.form['username']
        new_password = request.form['password']
        new_native_lang = request.form['native_lang']
        new_language = request.form['language']
        
        error = None

        if not new_username:
            error = 'Username is required.'
        elif not new_password:
            error = 'Password is required.'        
        


            #if username already exists in database
        if database.session.query(database.exists().where(User.username == new_username)).scalar():
            error = 'Username already exists.'

        if error is None:
            # ToDo:                
                # add error message
                # Need to set uId to a new number every time                


            # #add user to database
            # user = User(uId=2, username=new_username,report_status=0,ban_status=0,native_lang=new_native_lang,language=new_language)
            # user.set_password(new_password) #hashing done here to ensure plaintext is never inserted into the database
            # database.session.add(user)
            # database.session.commit()

            # if user.language == 'English':                                        #adding to english language
            #     user_lang = English(language = English, uId = user.uId,fluency=1)
            #     database.session.add(user_lang)
            #     database.session.commit()


            # Might be a better way to do this, but it will work for now
            # Pick last entry by uId then we increment
            userId = User.query.order_by(-User.uId).first()

            # Error checking if the query is empty
            if not userId:
                user = User(uId=0, username=new_username, password=generate_password_hash(new_password), report_status=0, ban_status=0, native_lang=new_native_lang)
            else:
                user = User(uId=userId.uId + 1, username=new_username, password=generate_password_hash(new_password), report_status=0, ban_status=0, native_lang=new_native_lang)
           
            language = Language(language=new_language, fluency=0)
            user.languages.append(language)

            database.session.add(user)
            database.session.commit()

            return redirect(url_for('auth.login'))

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
        
        user = User.query.filter_by(username = username).first()      
        error = None

        # Check username is in the databse
        # if not set error = "Incorrect Username or Password"
        if not user:
            return render_template('login.html', loginFailed = True)   

        # Check hashed password to matching username
        # if wrong set error = "Incorrect Username or Password"
        if check_password_hash(user.password, password):
            session["name"] = username
            return redirect(url_for('home.index'))
        
        return render_template('auth/login.html', loginFailed = True)

    return render_template('auth/login.html')

     # if error is None:
        #   session.clear()
        #   session['user_id'] = USERID FROM DATABASE
        #   return redirect(url_for('index'))
        
        #flash(error)      



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