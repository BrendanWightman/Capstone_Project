from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, make_response
)

gaming = Blueprint("gaming", __name__)

#Route for message landing page
@gaming.route('/test')
def test():
    return render_template('test.html')
