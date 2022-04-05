from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, make_response, session
)
from flask_socketio import join_room, leave_room, SocketIO
from .events import socketio
from .db import *

msg = Blueprint("msg", __name__)


#Route for message landing page
@msg.route('/msg', methods=('GET', 'POST'))
def landing():
    if request.method == 'POST':
        session['username'] = request.form['username'] #replace with loading user information or w/e
        target = request.form['target'] #will eventually replace with automated match based on preferences
        language = request.form['language']


        user = User.query.filter_by(username=session['username']).first()


        databaseMappings = {
            "French" : frenchHolding,
            "English" : englishHolding,
            "German" : germanHolding,
            "Japanese" : japaneseHolding,
            "Spanish" : spanishHolding
        }


        databaseHolding = databaseMappings[language]

        # Add all users to the holding room
        holding = databaseHolding(username=session['username'], roomId=language)
        database.session.add(holding)
        database.session.commit()   

        # Search if there exists an empty slot in a room that is already created
        # If so, join that room
        # else create a new room 

        profMappings = {
            "French" : French,
            "English" : English,
            "German" : German,
            "Japanese" : Japanese,
            "Spanish" : Spanish
        }

        profDatabase = profMappings[language]

        # Get proficiency in language
        userProf = profDatabase.query.filter_by(username=session['username']).first()
       
        # use a loop
        rooms = Rooms.query.filter_by(language=language).all()

        searchRange = 0
        foundRoom = False
        for room in rooms:
            if(room.proficiency + searchRange == userProf.fluency or room.proficiency - searchRange == userProf.fluency):
                room.initiator = user.username
                target = room.receiver
                database.session.commit()
                foundRoom = True
            else:
                searchRange += 1

        if(not foundRoom):
            newRoom = Rooms(receiver=session['username'], roomId=UNIQUE_ROOMID_CHANGE_LATER)
            database.session.add(newRoom)
            database.session.commit()
        




        # Enter username into holding room database
        # Take one user from holding room database and add to a 
        #   database with unique room id. Make user initiator
        # Randomly pick another user form the holding room database and 
        #   add their name in the other field of the entry


        if not username or not target: #Error Check
            return render_template('messaging/message_landing.html') #Add some kind of error message
        print(username + " is calling " + target)

        #Insert code to generate unique connection for WebRTC nonsense?

        #Cookie to store information about connection
        res = make_response(redirect(url_for('msg.msgChannel')))
        if(foundRoom):
            res.set_cookie(key="channel_info", value=username+":"+target+":"+"initiator")
        else:
            res.set_cookie(key="channel_info", value=username+":"+target+":"+"receiver")
        return res #Redirect user to their conversation channel
    return render_template('messaging/message_landing.html')

#consider adding between-page to hold users while they wait to be matched

#Route for actual communication between users
@msg.route('/channel', methods=('GET', 'POST'))
def msgChannel():

    #Handle Cookies:
    info = request.cookies.get('channel_info')
    if not info:
        #Add error message popup?
        return redirect(url_for('msg.landing'))
    user, target, identifier = info.split(':') #Once profiles exist load profile information

    #Bootleg way to determine who starts call
    if user == "John":
        temporary_identifier = "false"
    else:
        temporary_identifier = "true"
    #return render_template('messaging/message_channel.html', target=target, user=user, user_room="Test_Room", identity=temporary_identifier)
    room = Rooms.query.filter_by((initiator==user | receiver==user)).first()
    return render_template('messaging/message_channel.html', target=target, user=user, user_room=room.roomId, identity=identifier)
