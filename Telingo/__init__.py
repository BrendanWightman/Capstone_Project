import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from . import auth
from . import home
from db import database

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # 
    # When ready to deploy https://flask.palletsprojects.com/en/2.0.x/tutorial/deploy/
    # MAKE SURE TO CHANGE THIS
    #
    app.secret_key = 'dev'


    # Database config
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///Telingo.db'

    # I did not look into what these do and did not test with these options set.
    # app.config["SESSION_PERMANENT"] = False
    # app.config["SESSION_TYPE"] = "filesystem"

    # Not Sure how to use this, and it is not working. Figure it out later.
    #app.config.from_pyfile('config.py', silent=True)
    
    # Modular way to initialize the database
    database.app = app
    database.init_app(app)
    database.create_all()


    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(auth.auth)

    app.register_blueprint(home.home)
    app.add_url_rule('/', endpoint='index')

    app.register_error_handler(404, page_not_found)

    return app

def page_not_found(e):
  return render_template('404.html'), 404