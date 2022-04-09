from tkinter.tix import Form
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash



# The rest of the initilization is in __init__.py
database = SQLAlchemy()

# I think this needs to stay nullable if I understand it correctly.
# If not we can change it.
class User(database.Model):
    username  = database.Column(database.String(50), primary_key = True, unique=True,nullable = False)
    uId  = database.Column(database.Integer, nullable = False)
    password  = database.Column(database.String(200),nullable = True) 
    language = database.Column(database.String(50))
    native_lang = database.Column(database.String(50))
    report_status = database.Column(database.Integer())
    ban_status = database.Column(database.Integer())

    def __init__(self,username,uId,native_lang,language,report_status,ban_status):
        self.username= username
        self.uId = uId
        
        self.language = language
        self.native_lang = native_lang
        self.report_status = report_status
        self.ban_status = ban_status 

    
    
    #functions to create and check hashed passwords
    def set_password(self,pass2hash):
        self.password = generate_password_hash(pass2hash)

    def check_password(self,pass2check):
        return check_password_hash(self.password, pass2check)    

    #function to return a string when new data is added
    def __repr__(self):
        return '<name %r>' % self.username
  


#French language database
class French(database.Model):
    language = database.Column(database.String(50), primary_key = True)
    uId = database.Column(database.Integer())
    fluency = database.Column(database.Integer()) 


#English language database
class English (database.Model):
    language = database.Column(database.String(50), primary_key = True)
    uId = database.Column(database.Integer())
    fluency = database.Column(database.Integer()) 


#German language database
class German(database.Model):
    language = database.Column(database.String(50), primary_key = True)
    uId = database.Column(database.Integer())
    fluency = database.Column(database.Integer()) 


#Japanese language database
class Japanese(database.Model):
    language = database.Column(database.String(50), primary_key = True)
    uId = database.Column(database.Integer())
    fluency = database.Column(database.Integer()) 


#Spanish language database
class Spanish(database.Model):
    language = database.Column(database.String(50), primary_key = True)
    uId = database.Column(database.Integer())
    fluency = database.Column(database.Integer()) 


#Reporting database
class Report(database.Model):
    report_status = database.Column(database.Integer(), primary_key = True)
    reporter = database.Column(database.Integer()) 
    reportee = database.Column(database.Integer())


#Administrator
class Admin(database.Model):
    username = database.Column(database.Integer(), primary_key = True, unique=True)
    unique_id = database.Column(database.Integer())
    password  = database.Column(database.String(200))    
    
    #functions to create and check hashed passwords
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)    

    #function to return a string when new data is added
    def __repr__(self):
        return '<name %r>' % self.uId


