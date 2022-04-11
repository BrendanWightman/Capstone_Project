import os, requests, json

from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from flask_sqlalchemy import SQLAlchemy
from . import auth
from . import home
from . import msg
from .db import database

socketio = SocketIO()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    #
    # When ready to deploy https://flask.palletsprojects.com/en/2.0.x/tutorial/deploy/
    # MAKE SURE TO CHANGE THIS
    #
    app.secret_key = 'dev'

    #app.config.from_pyfile('config.py', silent=True)
    app.config.from_object('config')

    app.debug = 'debug'

    # Intialize SocketIO
    socketio.init_app(app)


  # Initialize the database
    database.app = app
    database.init_app(app)
    database.create_all()


    #Dictionary Lookup
    @socketio.on("Dictionary")
    def search_term(data):
        print('searching for term...')

        #Set up request based on data passed
        url = "https://lexicala1.p.rapidapi.com/search"
        querystring = {"text":data['text'],"language":data['language']}
        headers = {
        	"X-RapidAPI-Host": "lexicala1.p.rapidapi.com",
        	"X-RapidAPI-Key": ""
        }

        #Get result and convert into json format
        response = requests.request("GET", url, headers=headers, params=querystring)
        dict = response.json()

        #Check for no result
        if dict.get('n_results') == 0:
            emit('Dictionary-Response', {'text': "No Results Found"})
            return
        #Get result and send it
        definition = dict.get('results')[0].get('senses')[0].get("definition")
        emit('Dictionary-Response', {'text': definition})

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(auth.auth)

    app.register_blueprint(msg.msg)

    app.register_blueprint(home.home)
    app.add_url_rule('/', endpoint='index')

    app.register_error_handler(404, page_not_found)

    return app

def page_not_found(e):
  return render_template('404.html'), 404
