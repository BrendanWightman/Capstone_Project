import os, requests, json

from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from . import auth
from . import home
from . import msg

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    #
    # When ready to deploy https://flask.palletsprojects.com/en/2.0.x/tutorial/deploy/
    # MAKE SURE TO CHANGE THIS
    #
    app.secret_key = 'dev'

    app.config.from_pyfile('config.py', silent=True)
    socketio = SocketIO(app)
    socketio.run(app) #Look into alternative for this or w/e

    #SocketIO Listeners
    userCalls = {} #Dictionary to map UserIDs to their active calls
    @socketio.on("FirstConnect")
    def testFunction(data):
        print("User Joined: " + request.sid + " will be in room " + data['room'])
        userCalls[request.sid] = data['room']

    #Will get called a while after the user disconnects
    @socketio.on("disconnect")
    def disconnectFunction():
        print("User Left: " + request.sid)
        print("Cleaning up " + userCalls[request.sid])
        del userCalls[request.sid] #delete element from dictionary

    #Functions for Initiating Call
    @socketio.on("joinCallRoom")
    def joiningRoom(data):
        room = data['room']
        join_room(room)
        emit('maybeStart', to=room)
        print('joined room: ' + room)


    @socketio.on("startCall")
    def sendStartMessage(data):
        room = data['room']
        emit('startCall', to=room)
        print('sent start message')

    #Possible Leave-Room Function
    @socketio.on('leave')
    def on_leave(data):
        room = data['room']
        leave_room(room)
        print('leaving room: ' + room)

    #Message Passer (Needed for Signaling Server)
    @socketio.on("Message")
    def send_message(data):
        print('passing message')
        emit('Message', data, to=data['room'])

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
