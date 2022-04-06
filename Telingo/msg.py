from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, make_response
)
from flask_socketio import join_room, leave_room, SocketIO


msg = Blueprint("msg", __name__)


#Route for message landing page
@msg.route('/msg', methods=('GET', 'POST'))
def landing():
    if request.method == 'POST':
        username = request.form['username'] #replace with loading user information or w/e
        target = request.form['target'] #will eventually replace with automated match based on preferences

        if not username or not target: #Error Check
            return render_template('messaging/message_landing.html') #Add some kind of error message
        print(username + " is calling " + target)

        #Insert code to generate unique connection for WebRTC nonsense?

        #Cookie to store information about connection
        res = make_response(redirect(url_for('msg.msgChannel')))
        res.set_cookie(key="channel_info", value=username+":"+target)
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
    user, target = info.split(':') #Once profiles exist load profile information

    #Bootleg way to determine who starts call
    if user == "John":
        temporary_identifier = "false"
    else:
        temporary_identifier = "true"
    #Temp language is always english, make sure you use 2 char identifier
    language = "en"

    return render_template('messaging/message_channel.html', target=target, user=user, user_room="Test_Room", identity=temporary_identifier, language=language)
