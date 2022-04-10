from flask_sqlalchemy import SQLAlchemy
#from werkzeug.security import check_password_hash, generate_password_hash



# The rest of the initilization is in __init__.py
database = SQLAlchemy()
    
class User(database.Model):
    username  = database.Column(database.String(50), primary_key = True, unique=True,nullable = False)
    uId  = database.Column(database.Integer, nullable = False)
    password  = database.Column(database.String(200),nullable = True)
    native_lang = database.Column(database.String(50))
    report_status = database.Column(database.Integer)
    ban_status = database.Column(database.Integer)
    languages = database.relationship('Language', backref=database.backref('user', lazy=True))
    rooms = database.relationship('Room', backref=database.backref('user', lazy=True))
    def __repr__(self):
        return '<User %r>' % self.username

class Language(database.Model):
    uId  = database.Column(database.Integer, database.ForeignKey('user.uId'), nullable = False, primary_key = True,)
    language = database.Column(database.String(50), primary_key = True)
    fluency = database.Column(database.Integer)   

class Room(database.Model):
    roomId = database.Column(database.Integer(), primary_key = True, unique=True)
    language = database.Column(database.String(50))
    initiator = database.Column(database.String(50))
    receiver = database.Column(database.String(50))
    proficiency = database.Column(database.Integer())

class HoldingRoom(database.Model):
    username = database.Column(database.Integer(), primary_key = True, unique=True)
    language = database.Column(database.String(50))


# Example of a language query
# Language.query.with_parent(user).filter(Language.language == 'French').all()
# Returns the results of "user's" Language where language = 'French'


# #Reporting database
# class Report(database.Model):
#     report_status = database.Column(database.Integer, primary_key = True)
#     reporter = database.Column(database.Integer) 
#     reportee = database.Column(database.Integer)

# #Administrator
# class Admin(database.Model):
#     username = database.Column(database.Integer(), primary_key = True, unique=True)
#     unique_id = database.Column(database.Integer())
#     password  = database.Column(database.String(200))
#     def __repr__(self):
#         return '<Admin %r>' % self.username    

# # Language Holding Rooms
# class frenchHolding(database.Model):
#     username = database.Column(database.Integer(), primary_key = True, unique=True)  

# class englishHolding(database.Model):
#     username = database.Column(database.Integer(), primary_key = True, unique=True)  

# class germanHolding(database.Model):
#     username = database.Column(database.Integer(), primary_key = True, unique=True)  

# class japaneseHolding(database.Model):
#     username = database.Column(database.Integer(), primary_key = True, unique=True)  

# class spanishHolding(database.Model):
#     username = database.Column(database.Integer(), primary_key = True, unique=True)  

# class Rooms(database.Model):
#     roomId = database.Column(database.Integer(), primary_key = True, unique=True)
#     language = database.Column(database.String(50))
#     initiator = database.Column(database.String(50))
#     receiver = database.Column(database.String(50))
#     proficiency = database.Column(database.Integer())
