from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


# The rest of the initilization is in __init__.py
database = SQLAlchemy()

# I think this needs to stay nullable if I understand it correctly.
# If not we can change it.
class User(database.Model):
    username  = database.Column(database.String(50), primary_key = True, unique=True,nullable = False)
    uId  = database.Column(database.Integer, nullable = False)
    password  = database.Column(database.String(200), nullable = False) 
    native_lang = database.Column(database.String(50))
    report_status = database.Column(database.Integer(), default=0)
    ban_status = database.Column(database.Integer(), default=0)
    languages = database.relationship('French','English','German','Japanese','Spanish', backref ='user')

    def __init__(self,username,uId,password,native_lang,report_status,ban_status):
        self.username= username
        self.uId = uId
        self.password = password     
        self.native_lang = native_lang
        self.report_status = report_status
        self.ban_status = ban_status
    
    #functions to create and check hashed passwords
    def set_password(password):
        password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)    

    #function to return a string when new data is added
    def __repr__(self):
        return '<name %r>' % self.uId
  


#French language database
class French(database.Model):
    language = database.Column(database.String(50), primary_key = True)
    uId = database.Column(database.Integer(), database.ForeignKey('user.uId'))
    fluency = database.Column(database.Integer()) 


#English language database
class English (database.Model):
    language = database.Column(database.String(50), primary_key = True)
    uId = database.Column(database.Integer(), database.ForeignKey('user.uId'))
    fluency = database.Column(database.Integer()) 


#German language database
class German(database.Model):
    language = database.Column(database.String(50), primary_key = True)
    uId = database.Column(database.Integer(), database.ForeignKey('user.uId'))
    fluency = database.Column(database.Integer()) 


#Japanese language database
class Japanese(database.Model):
    language = database.Column(database.String(50), primary_key = True)
    uId = database.Column(database.Integer(), database.ForeignKey('user.uId'))
    fluency = database.Column(database.Integer()) 


#Spanish language database
class Spanish(database.Model):
    language = database.Column(database.String(50), primary_key = True)
    uId = database.Column(database.Integer(), database.ForeignKey('user.uId'))
    fluency = database.Column(database.Integer()) 


#Reporting database
class Report(database.Model):
    report_status = database.Column(database.Integer(), primary_key = True)
    reporter = database.Column(database.Integer(), database.ForeignKey('user.uId')) 
    reportee = database.Column(database.Integer(), database.ForeignKey('user.uId'))


#Administrator
class Admin(database.Model):
    username = database.Column(database.Integer(), primary_key = True, unique=True)
    unique_id = database.Column(database.Integer())
    password  = database.Column(database.String(200))    

# Language Holding Rooms
class frenchHolding(database.Model):
    username = database.Column(database.Integer(), primary_key = True, unique=True)  

class englishHolding(database.Model):
    username = database.Column(database.Integer(), primary_key = True, unique=True)  

class germanHolding(database.Model):
    username = database.Column(database.Integer(), primary_key = True, unique=True)  

class japaneseHolding(database.Model):
    username = database.Column(database.Integer(), primary_key = True, unique=True)  

class spanishHolding(database.Model):
    username = database.Column(database.Integer(), primary_key = True, unique=True)  

class Rooms(database.Model):
    roomId = database.Column(database.Integer(), primary_key = True, unique=True)
    language = database.Column(database.String(50))
    initiator = database.Column(database.String(50))
    receiver = database.Column(database.String(50))
    proficiency = database.Column(database.Integer())
