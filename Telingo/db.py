#from tkinter.tix import Form
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
    def __repr__(self):
        return '<User %r>' % self.username

class Language(database.Model):
    uId  = database.Column(database.Integer, database.ForeignKey('user.uId'), nullable = False, primary_key = True,)
    language = database.Column(database.String(50), primary_key = True)
    fluency = database.Column(database.Integer)   

# Example of a language query
# Language.query.with_parent(user).filter(Language.language == 'French').all()
# Returns the results of "user's" Language where language = 'French'


#Reporting database
class Report(database.Model):
    report_status = database.Column(database.Integer, primary_key = True)
    reporter = database.Column(database.Integer) 
    reportee = database.Column(database.Integer)

#Administrator
class Admin(database.Model):
    username = database.Column(database.Integer(), primary_key = True, unique=True)
    unique_id = database.Column(database.Integer())
    password  = database.Column(database.String(200))
    def __repr__(self):
        return '<Admin %r>' % self.username

# # I think this needs to stay nullable if I understand it correctly.
# # If not we can change it.
# class User(database.Model):
#     username  = database.Column(database.String(50), primary_key = True, unique=True,nullable = False)
#     uId  = database.Column(database.Integer, nullable = False)
#     password  = database.Column(database.String(200),nullable = True) 
#     language = database.Column(database.String(50))
#     native_lang = database.Column(database.String(50))
#     report_status = database.Column(database.Integer())
#     ban_status = database.Column(database.Integer())

#     def __init__(self,username,uId,native_lang,language,report_status,ban_status):
#         self.username= username
#         self.uId = uId               
#         self.language = language
#         self.native_lang = native_lang
#         self.report_status = report_status
#         self.ban_status = ban_status     

#     #functions to create and check hashed passwords
#     def set_password(self,pass2hash):
#         self.password = generate_password_hash(pass2hash)

#     def check_password(self,pass2check):
#         return check_password_hash(self.password, pass2check)    

#     #function to return a string when new data is added
#     def __repr__(self):
#         return '<name %r>' % self.username
  


# #French language database
# class French(database.Model):
#     language = database.Column(database.String(50), primary_key = True)
#     uId = database.Column(database.Integer())
#     fluency = database.Column(database.Integer()) 

#     def __init__(self,language,uId,fluency):
#         self.language = language
#         self.uId = uId
#         self.fluency = fluency
        


# #English language database
# class English (database.Model):
#     language = database.Column(database.String(50), primary_key = True)
#     uId = database.Column(database.Integer())
#     fluency = database.Column(database.Integer()) 

#     def __init__(self,language,uId,fluency):
#         self.language = language
#         self.uId = uId
#         self.fluency = fluency


# #German language database
# class German(database.Model):
#     language = database.Column(database.String(50), primary_key = True)
#     uId = database.Column(database.Integer())
#     fluency = database.Column(database.Integer())

#     def __init__(self,language,uId,fluency):
#         self.language = language
#         self.uId = uId
#         self.fluency = fluency 


# #Japanese language database
# class Japanese(database.Model):
#     language = database.Column(database.String(50), primary_key = True)
#     uId = database.Column(database.Integer())
#     fluency = database.Column(database.Integer()) 

#     def __init__(self,language,uId,fluency):
#         self.language = language
#         self.uId = uId
#         self.fluency = fluency


# #Spanish language database
# class Spanish(database.Model):
#     language = database.Column(database.String(50), primary_key = True)
#     uId = database.Column(database.Integer())
#     fluency = database.Column(database.Integer()) 

#     def __init__(self,language,uId,fluency):
#         self.language = language
#         self.uId = uId
#         self.fluency = fluency


# #Reporting database
# class Report(database.Model):
#     report_status = database.Column(database.Integer(), primary_key = True)
#     reporter = database.Column(database.Integer()) 
#     reportee = database.Column(database.Integer())

#     def __init__(self,report_Status,reporter,reportee):
#         self.report_status = report_Status
#         self.reporter = reporter
#         self.reportee = reportee


# #Administrator
# class Admin(database.Model):
#     username = database.Column(database.Integer(), primary_key = True, unique=True)
#     unique_id = database.Column(database.Integer())
#     password  = database.Column(database.String(200))    
    
#     def __init__(self,username,unique_id):
#         self.username = username
#         self.unique_id = unique_id

#     #functions to create and check hashed passwords
#     def set_password(self,pass2hash):
#         self.password = generate_password_hash(pass2hash)

#     def check_password(self,pass2check):
#         return check_password_hash(self.password,pass2check)    

#     #function to return a string when new data is added
#     def __repr__(self):
#         return '<name %r>' % self.username


