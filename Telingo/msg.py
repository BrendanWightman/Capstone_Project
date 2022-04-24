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
    if not ('username' in session): #If not logged in, send to login page
        return make_response(redirect(url_for('auth.login')))

    if request.method == 'GET': #Get second language info for default form values
        user = User.query.filter_by(username = session['username']).first()
        secondLanguage = Language.query.with_parent(user).first()
        return render_template('messaging/skillselect.html', secondLanguage=secondLanguage)

    elif request.method == 'POST':
        #Pull language from form
        language = request.form['language']

        #get user from table + reset roomId
        user = User.query.filter_by(username=session['username']).first()

        #If the user's language is declared, use their proficiency; otherwise use the one from the form
        uLanguage = Language.query.with_parent(user).filter(Language.language == language).first()
        if not uLanguage:
            fluency = int(request.form['skillLevel'])
        else:
            fluency = uLanguage.fluency

        #Debug Print
        print("Matching a user in " + language + " with skill level: " + str(fluency))


        # Check to see if user is already in a room
        checkRoom = Room.query.filter((Room.initiator == user.username) | (Room.receiver == user.username)).first()
        if(checkRoom is not None):
            database.session.delete(checkRoom)
            database.session.commit()

        rooms = Room.query.filter(Room.language == language).all()

        # if room exists that is same language, join room
        # else create room

        searchRange = 0
        foundRoom = False


        if(rooms is not None):
            while (not foundRoom and searchRange < 6): #change number if fluency range smaller
                #print("Searching on range " + str(fluency - searchRange) + " : " + str(fluency + searchRange))
                for room in rooms:
                    # Make this part of the query?
                    # Add searching for only your native speakers
                    if((room.receiverFluency + searchRange == fluency or room.receiverFluency - searchRange == fluency) and room.language == language and room.initiator == None and not foundRoom):
                        room.initiator = session['username']
                        room.initiatorFluency = fluency
                        database.session.commit()
                        session['roomId'] = room.roomId
                        foundRoom = True
                #time.sleep(2)
                searchRange += 1

        if(not foundRoom):
            roomId = Room.query.order_by(-Room.roomId).first()

            # Error checking if the query is empty
            if not roomId:
                uRoom = Room(roomId=0, language=language, receiverFluency=fluency, receiver=session['username'], initiator=None, initiatorFluency=None)
            else:
                uRoom = Room(roomId=roomId.roomId + 1, language=language, receiverFluency=fluency, receiver=session['username'], initiator=None, initiatorFluency=None)

            session['roomId'] = uRoom.roomId

            database.session.add(uRoom)
            database.session.commit()

        #Cookie to store information about connection
        # Might not need this anymore
        res = make_response(redirect(url_for('msg.msgHolding')))
        return res #Redirect user to their conversation channel
    return render_template('messaging/skillselect.html')


# Loading room
@msg.route('/holding', methods=('GET', 'POST'))
def msgHolding():
    if not ('username' in session): #If not logged in, send to login page
        return make_response(redirect(url_for('auth.login')))

    #load room info and send to corresponding page
    room = Room.query.filter(((Room.initiator==session['username']) | (Room.receiver==session['username']))).first()
    if(room.initiator==session['username']):
        return render_template('messaging/middleman.html', user=session['username'],target=room.receiver, user_room=room.roomId, identity="true")
    else:
        return render_template('messaging/middleman.html', user=session['username'],target=room.initiator, user_room=room.roomId, identity="false")


#Route for actual communication between users
@msg.route('/channel', methods=('GET', 'POST'))
def msgChannel():
    if not ('username' in session): #If not logged in, send to login page
        return make_response(redirect(url_for('auth.login')))

    if request.method == 'GET':
        #Safety check to prevent direct URL access
        if not ('roomId' in session):
            return redirect(url_for('msg.landing'))

        #Generate topic suggestions based on random number
        rand = random.randint(0, (len(topics)/4)-1) * 4
        top1 = topics[rand]
        top2 = topics[rand+1]
        top3 = topics[rand+2]
        top4 = topics[rand+3]

        #Languages map for dictionary API
        shortLanguage = {
            "French" : "fr",
            "English" : "en",
            "German" : "de",
            "Japanese" : "ja",
            "Spanish" : "es",
        }

        #First load room data + store for use
        room = Room.query.filter(((Room.initiator==session['username']) | (Room.receiver==session['username']))).first()
        if not room: #If the room not found, some kind of error has occured so redirect to landing
            return make_response(redirect(url_for('msg.landing')))

        language = shortLanguage[room.language]
        user_room=room.roomId
        if(room.initiator==session['username']):
            target=room.receiver
            identity="true"
            targetsFluency=room.receiverFluency
        else:
            target=room.initiator
            identity="false"
            targetsFluency=room.initiatorFluency

        # Get the other target's language proficiency to display to user


        #If flagged, delete | otherwise, set flag for other user to delete
        if room.already_deleted:
            database.session.delete(room)
            database.session.commit()
        else:
            room.already_deleted = True
            database.session.commit()
        del session['roomId']
        #Use saved data to render template
        return render_template('messaging/message_channel.html', user=session['username'],target=target, targetsFluency=targetsFluency, language=language, user_room=user_room, identity=identity, top1=top1, top2=top2, top3=top3, top4=top4)

    elif request.method == 'POST':
        print('We got a Post Method')
        if(int(request.form['ReportUser']) != 0):
            #Add report to database
            reportGet = Report.query.order_by(-Report.report_id).first()
            reportID = 0
            if reportGet:
                reportID = reportGet.report_id + 1
            newReport = Report(report_id = reportID, report_status = request.form['ReportUser'], reporter = request.form['user'], reportee = request.form['target'])
            database.session.add(newReport)
            database.session.commit()
        else:
            print('No Report Needed')
        return make_response(redirect(url_for('msg.landing')))
