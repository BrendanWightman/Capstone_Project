import os, requests, json

from flask import Flask, render_template
from flask_socketio import SocketIO
from . import auth
from . import home
from . import msg
from .db import database

socketio = SocketIO()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Change this for deployment to a random string
    app.secret_key = 'dev'

    # Set configuations from config.py
    app.config.from_object('config')

    # Change this for deployment
    app.debug = 'debug'

    # Intialize SocketIO
    socketio.init_app(app)


  # Initialize the database
    database.app = app
    database.init_app(app)
    database.create_all()


    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # Blueprint registration
    app.register_blueprint(auth.auth)

    app.register_blueprint(msg.msg)

    app.register_blueprint(home.home)
    app.add_url_rule('/', endpoint='index')

    app.register_error_handler(404, page_not_found)

    return app

def page_not_found(e):
  return render_template('404.html'), 404

