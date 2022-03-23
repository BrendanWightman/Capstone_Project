from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


# The rest of the initilization is in __init__.py
database = SQLAlchemy()

# I think this needs to stay nullable if I understand it correctly.
# If not we can change it.
class User(database.Model):
    username  = database.Column(database.String(50), primary_key = True, unique=True, nullable = False)
    uId  = database.Column(database.Integer, nullable = False)
    password  = database.Column(database.String(200), nullable = False)    
    
    #functions to create and check hashed passwords
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)    

    #function to return a string when new data is added
    def __repr__(self):
        return '<name %r>' % self.uId


#User ID database
class User_ID (database.Model):
    uId = database.Column(database.Integer, primary_key = True, nullable = False)
    language = database.Column(database.String(50), nullable = False)
    native_lang = database.Column(database.String(50), nullable = False)
    report_status = database.Column(database.Integer(20), nullable = False)
    ban_status = database.Column(database.Integer(5), nullable = False)


#French language database
class French(database.Model):
    language = database.Column(database.String(50), primary_key = True, nullable = False)
    uId = database.Column(database.Integer, nullable = False) 
    fluency = database.Column(database.Integer(10), nullable = False) 


#English language database
class English (database.Model):
    language = database.Column(database.String(50), primary_key = True, nullable = False)
    uId = database.Column(database.Integer, nullable = False) 
    fluency = database.Column(database.Integer(10), nullable = False) 


#German language database
class German(database.Model):
    language = database.Column(database.String(50), primary_key = True, nullable = False)
    uId = database.Column(database.Integer, nullable = False) 
    fluency = database.Column(database.Integer(10), nullable = False) 


#Japanese language database
class Japanese(database.Model):
    language = database.Column(database.String(50), primary_key = True, nullable = False)
    uId = database.Column(database.Integer, nullable = False) 
    fluency = database.Column(database.Integer(10), nullable = False) 


#Spanish language database
class Spanish(database.Model):
    language = database.Column(database.String(50), primary_key = True, nullable = False)
    uId = database.Column(database.Integer, nullable = False) 
    fluency = database.Column(database.Integer(10), nullable = False) 


#Reporting database
class Report(database.Model):
    report_status = database.Column(database.Integer(20), primary_key = True, nullable = False)
    reporter = database.Column(database.Integer(20), nullable = False) 
    reportee = database.Column(database.Integer(20), nullable = False) 


#Administrator
class Admin(database.Model):
    username = database.Column(database.Integer(20), primary_key = True, unique=True, nullable = False)
    unique_id = database.Column(database.Integer(20), nullable = False)
    password  = database.Column(database.String(200), nullable = False)    
    
    #functions to create and check hashed passwords
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)    

    #function to return a string when new data is added
    def __repr__(self):
        return '<name %r>' % self.uId


