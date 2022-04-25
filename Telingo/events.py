from flask_socketio import SocketIO, join_room, leave_room, send, emit
import requests, json
from flask import url_for, request, session
from . import socketio
from .db import *

#SocketIO Listeners
userQueue = {}
@socketio.on("registerExistence")
def registerInformation():
    userQueue[request.sid] = True

@socketio.on("cleanExistence")
def registerInformation():
    del userQueue[request.sid]

@socketio.on("disconnect")
def disconnectFunction():
    #Delete for unclean middleman leave:
    if request.sid in userQueue:
        roomDb =  Room.query.filter((Room.initiator==session['username']) | (Room.receiver==session['username'])).first()
        if roomDb is not None:
            print(f"Deleting {roomDb} due to middleman leave")
            database.session.delete(roomDb)
            database.session.commit()
        del userQueue[request.sid]

@socketio.on("transfer")
def transfer(data):
    room = data['room']
    emit('transferPage', url_for('msg.msgChannel'), to=room)

@socketio.on("beginMatch")
def matchUsers(data):
    language = data['language']
    fluency = data['fluency']
    roomId = None
    # Check to see if user somehow already in a room, if so delete that room
    user = User.query.filter_by(username=session['username']).first()
    checkRoom = Room.query.filter((Room.initiator == user.username) | (Room.receiver == user.username)).first()
    if(checkRoom is not None):
        database.session.delete(checkRoom)
        database.session.commit()

    rooms = Room.query.filter(Room.language == language).all()

    # if room exists that is same language, join room
    # else create room

    searchRange = 0
    foundRoom = False

    if(rooms): #If a room exists, we need to search through them
        while (not foundRoom and searchRange < 6): #change number if fluency range changes
            #print("Searching on range " + str(fluency - searchRange) + " : " + str(fluency + searchRange))
            for room in rooms:
                # Make this part of the query?
                # Add searching for only your native speakers
                if((room.receiverFluency + searchRange == fluency or room.receiverFluency - searchRange == fluency) and room.language == language and room.initiator == None and not foundRoom):
                    room.initiator = session['username'] # POSSIBLE ERROR SPOT
                    room.initiatorFluency = fluency
                    database.session.commit()
                    roomId = room.roomId
                    foundRoom = True
            searchRange += 1

    if(not foundRoom):
        roomId = Room.query.order_by(-Room.roomId).first()

        # Error checking if the query is empty
        if not roomId:
            uRoom = Room(roomId=0, language=language, receiverFluency=fluency, receiver=session['username'], initiator=None, initiatorFluency=None)
        else:
            uRoom = Room(roomId=roomId.roomId + 1, language=language, receiverFluency=fluency, receiver=session['username'], initiator=None, initiatorFluency=None)

        roomId = uRoom.roomId

        database.session.add(uRoom)
        database.session.commit()

    emit('finishedMatching', {'roomId': (roomId)}, broadcast=False)


#Functions for Initiating Call
@socketio.on("joinCallRoom")
def joiningRoom(data):
    room = data['room']
    join_room(room)
    emit('maybeStart', to=room)
    print('joined room: ' + str(room))

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
    response = requests.request("GET", url, headers=headers, params=querystring)
    dict = response.json()

    #Check for no result
    if dict.get('n_results') == 0:
        emit('Dictionary-Response', {'text': "No Results Found"})
        return
    #Get result and send it
    definition = dict.get('results')[0].get('senses')[0].get("definition")
    emit('Dictionary-Response', {'text': definition})
