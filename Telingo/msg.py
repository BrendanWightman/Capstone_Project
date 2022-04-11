import json, random
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, make_response, session
)
from flask_socketio import join_room, leave_room, SocketIO, emit
from .db import *

msg = Blueprint("msg", __name__)
#Open and load file for random topics, maybe change later
topics_f = open('Telingo/static/conversation_topics.json')
topics = json.load(topics_f).get('topics')
topics_f.close()

#Route for message landing page
@msg.route('/msg', methods=('GET', 'POST'))
def landing():
    if request.method == 'POST':
        session['username'] = request.form['username'] #replace with loading user information or w/e
        target = request.form['target'] #will eventually replace with automated match based on preferences
        language = request.form['language']

        user = User.query.filter_by(username=session['username']).first()
        session['roomId'] = None

        # Check to see if user is already in a room
        checkRoom = Room.query.filter((Room.initiator == user.username) | (Room.receiver == user.username)).first()
        if(checkRoom is not None):
            database.session.delete(checkRoom)
            database.session.commit()

        uLanguage = Language.query.with_parent(user).filter(Language.language == language).first()

        print(uLanguage.fluency)

        rooms = Room.query.filter(Room.language == language).all()

        # if room exists that is same language, join room
        # else create room

        searchRange = 0
        foundRoom = False

        if(rooms is not None):
            while (not foundRoom and searchRange < 10): #change number if fluency range smaller
                for room in rooms:
                    # Make this part of the query?
                    # Add searching for only your native speakers
                    if((room.fluency + searchRange == uLanguage.fluency or room.fluency - searchRange == uLanguage.fluency) and room.language == language and room.initiator == None and not foundRoom):
                        room.initiator = session['username']
                        database.session.commit()
                        session['roomId'] = room.roomId
                        foundRoom = True
                searchRange += 1

        if(not foundRoom):
            roomId = Room.query.order_by(-Room.roomId).first()

            # Error checking if the query is empty
            if not roomId:
                uRoom = Room(roomId=0, language=language, fluency=uLanguage.fluency, receiver=session['username'], initiator=None)
            else:
                uRoom = Room(roomId=roomId.roomId + 1, language=language, fluency=uLanguage.fluency, receiver=session['username'], initiator=None)

            session['roomId'] = uRoom.roomId

            database.session.add(uRoom)
            database.session.commit()

        #Cookie to store information about connection
        # Might not need this anymore
        res = make_response(redirect(url_for('msg.msgHolding')))
        if(foundRoom):
            res.set_cookie(key="channel_info", value=session['username']+":"+"initiator")
        else:
            res.set_cookie(key="channel_info", value=session['username']+":"+"receiver")
        return res #Redirect user to their conversation channel
    return render_template('messaging/message_landing.html')


# Loading room
@msg.route('/holding', methods=('GET', 'POST'))
def msgHolding():
    room = Room.query.filter(((Room.initiator==session['username']) | (Room.receiver==session['username']))).first()
    if(room.initiator==session['username']):
        return render_template('messaging/middleman.html', user=session['username'],target=room.receiver, user_room=room.roomId, identity="true")
    else:
        return render_template('messaging/middleman.html', user=session['username'],target=room.initiator, user_room=room.roomId, identity="false")


#Route for actual communication between users
@msg.route('/channel', methods=('GET', 'POST'))
def msgChannel():

    #Handle Cookies:
    info = request.cookies.get('channel_info')
    if not info:
        #Add error message popup?
        return redirect(url_for('msg.landing'))

    #Double check there isn't a more efficient way to do this
    rand = random.randint(0, (len(topics)/4)-1) * 4
    top1 = topics[rand]
    top2 = topics[rand+1]
    top3 = topics[rand+2]
    top4 = topics[rand+3]

    room = Room.query.filter(((Room.initiator==session['username']) | (Room.receiver==session['username']))).first()
    if(room.initiator==session['username']):
        return render_template('messaging/message_channel.html', user=session['username'],target=room.receiver, user_room=room.roomId, identity="true", top1=top1, top2=top2, top3=top3, top4=top4)
    else:
        return render_template('messaging/message_channel.html', user=session['username'],target=room.initiator, user_room=room.roomId, identity="false", top1=top1, top2=top2, top3=top3, top4=top4)
