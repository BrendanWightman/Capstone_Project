from flask_socketio import SocketIO, join_room, leave_room, send, emit
from flask import url_for, request, session
from . import socketio
from .db import *

#SocketIO Listeners
userCalls = {} #Dictionary to map UserIDs to their active calls
@socketio.on("FirstConnect")
def testFunction(data):
    if 'room' in data:
        print("User Joined: " + request.sid + " will be in room " + data['room'])
        userCalls[request.sid] = data['room']

@socketio.on("disconnect")
def disconnectFunction():
    print("User Left: " + request.sid)
    if request.sid in userCalls:
        print("Cleaning up " + userCalls[request.sid])
        emit('transferPage', url_for('msg.landing'), to=session['roomId'])
        del userCalls[request.sid] #delete element from dictionary

@socketio.on("transfer")
def transfer(data):
    room = data['room']
    emit('transferPage', url_for('msg.msgChannel'), to=room)

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
    # Delete entry in database
    if room is not None:
        print(f"Deleting {room}")
        if(room.initiator == session['roomId']):
            room.initiator = None
        if(room.receiver == session['roomId'] and room.initiator == None):
            database.session.delete(room)
        database.session.commit()
        session['roomId'] = None
    leave_room(room)
    print('leaving room: ' + room)

#Message Passer (Needed for Signaling Server)
@socketio.on("Message")
def send_message(data):
    print('passing message')
    emit('Message', data, to=data['room'])

#Function to communicate that they are out of Ice candidates
@socketio.on("outOfIce")
def out_of_ice(data):
    room = data['room']
    print("User out of ICE candidates")
    emit('noIce', to=room)

@socketio.on("allOutOfIce")
def sendTerminate(data):
    print("All out of candidates, terminating call")
    room = data['room']
    emit('terminateNoIce', to=room)

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
    response = request.request("GET", url, headers=headers, params=querystring)
    dict = response.json()

    #Check for no result
    if dict.get('n_results') == 0:
        emit('Dictionary-Response', {'text': "No Results Found"})
        return
    #Get result and send it
    definition = dict.get('results')[0].get('senses')[0].get("definition")
    emit('Dictionary-Response', {'text': definition})
