import os

from flask import Flask, render_template
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
    @socketio.on("FirstConnect")
    def testFunction(data):
        print('recieved: ' + data['info']) #Can remove / replace with any first-connection function

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
