from flask import ( Blueprint, flash, g, redirect,
 render_template, request, session, url_for, make_response)
from password_validation import PasswordPolicy
from werkzeug.security import check_password_hash, generate_password_hash

from .db import Admin, Language, database, User, Report

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
        policy = PasswordPolicy()

        if not new_username:
            error = 'Username is required.'
        elif not new_password:
            error = 'Password is required.'

        elif not policy.validate(new_password):   #policy is 8 characters with at least 1 number. edited in policy.py.
            for requirement in policy.test_password(new_password):
                alert = f"{requirement.name} not satisfied: expected: {requirement.requirement}, got: {requirement.actual}"
                flash(alert)
                return redirect(url_for('auth.register'))


            #if username already exists in database
        if database.session.query(database.exists().where(User.username == new_username)).scalar():
            error = 'Username already exists.'
            return redirect(url_for('auth.login'))

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

    return render_template("/auth/register.html")



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
            return render_template('/auth/login.html', loginFailed = True)

        # Check ban status of user
        user = User.query.filter_by(username = username).first()
        if(user.ban_status != 0):
            alert = 'Your account has been disabled.'
            flash(alert)
            return redirect(url_for('auth.login'))

        # Check hashed password to matching username
        # if wrong set error = "Incorrect Username or Password"
        if check_password_hash(user.password, password):
            session["username"] = username
            return redirect(url_for('home.index'))

        return render_template('/auth/login.html', loginFailed = True)

    return render_template('/auth/login.html')

     # if error is None:
        #   session.clear()
        #   session['user_id'] = USERID FROM DATABASE
        #   return redirect(url_for('index'))
        #flash(error)


#
#Admin login page
#

@auth.route('/adminlogin', methods=('GET', 'POST'))
def adminlogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check admin exists in database with 'username'
        admin = Admin.query.filter_by(username = username).first()

        # if not found return to login
        if not admin:
            return render_template('auth/adminlogin.html', loginFailed=True)

        if check_password_hash(admin.password, password):
            session["admin_username"] = username
            return redirect(url_for('auth.ban'))
            
        return render_template('auth/admin.html', loginFailed = True)

    return render_template('auth/adminlogin.html')

#
#Admin ban page
#

@auth.route('/admin', methods = ('GET','POST'))
def ban():
    if not ('admin_username' in session): #If not logged in, send to admin login page
        return make_response(redirect(url_for('auth.adminlogin')))
            
    # When page is rendered get a list of all reported users
    if request.method == 'GET':
        users = Report.query.order_by(Report.report_id).all()
        return render_template('auth/admin.html', users=users)
    
    # When the admin submits a username for ban
    # check if username is a user and set ban_status to 1
    # if the username is incorrect, alert the admin
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username = username).first()
        if user is not None:
            user.ban_status = 1
            database.session.commit()
        else:
            alert = 'User Does Not Exist'
            flash(alert)
    return redirect(url_for('auth.ban'))

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))