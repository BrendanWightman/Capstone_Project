from flask import Flask, app
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy


#
#Database Initialization
#
db = SQLAlchemy(app)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Telingo.db'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


Session(app)

class User(db.Model):
    username  = db.Column(db.string(200),primary_key = True)
    password  = db.Column(db.String(200),  nullable = True)
    language      = db.Column(db.String(200),  nullable = True)

    def __init__(self,username, password,language):
        self.username = username
        self.password = password
        self.language = language

 #function to return a string when new data is added
    def __repr__(self):
        return '<name %r>' % self.id