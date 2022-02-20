from flask import (
    Blueprint, render_template
)

msg = Blueprint("msg", __name__)

@msg.route('/msg/')
def landing():
    return render_template('messaging.html')
