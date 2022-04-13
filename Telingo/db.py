from flask_sqlalchemy import SQLAlchemy

# The rest of the initilization is in __init__.py
database = SQLAlchemy()
    
class User(database.Model):
    uId  = database.Column(database.Integer, primary_key = True,  nullable = False)
    username  = database.Column(database.String(50), unique=True,nullable = False)
    password  = database.Column(database.String(200),nullable = True)
    native_lang = database.Column(database.String(50))
    report_status = database.Column(database.Integer)
    ban_status = database.Column(database.Integer)
    languages = database.relationship('Language', backref=database.backref('user', lazy=True))
    def __repr__(self):
        return '<User %r>' % self.username

class Language(database.Model):
    uId  = database.Column(database.Integer, database.ForeignKey('user.uId'), nullable = False, primary_key = True,)
    language = database.Column(database.String(50), primary_key = True)
    fluency = database.Column(database.Integer)   

# Example of a language query
# Language.query.with_parent(user).filter(Language.language == 'French').all()
# Returns the results of "user's" Language where language = 'French'


class Room(database.Model):
    roomId = database.Column(database.Integer(), primary_key = True, unique=True)
    language = database.Column(database.String(50))
    initiator = database.Column(database.String(50), nullable = True) # Change to uId if we can figure it out
    receiver = database.Column(database.String(50), nullable = False)

    fluency = database.Column(database.Integer())

#Reporting database
class Report(database.Model):
    report_id = database.Column(database.Integer, primary_key = True)
    report_status = database.Column(database.Integer)
    reporter = database.Column(database.String(50))
    reportee = database.Column(database.String(50))

#Administrator
class Admin(database.Model):
    uId  = database.Column(database.Integer, primary_key = True,  nullable = False)
    username = database.Column(database.Integer(), unique=True)
    password  = database.Column(database.String(200))
    def __repr__(self):
        return '<Admin %r>' % self.username
