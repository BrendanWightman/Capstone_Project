from flask_socketio import SocketIO, join_room, leave_room, send, emit
from . import socketio

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