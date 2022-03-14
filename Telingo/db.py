from flask_sqlalchemy import SQLAlchemy


# The rest of the initilization is in __init__.py
database = SQLAlchemy()

# I think this needs to stay nullable if I understand it correctly.
# If not we can change it.
class User(database.Model):
    uId  = database.Column(database.Integer, primary_key = True)
    username  = database.Column(database.String(200), nullable = False)
    password  = database.Column(database.String(200), nullable = False)
    #language  = database.Column(database.String(200), nullable = False)

 #function to return a string when new data is added
    def __repr__(self):
        return '<name %r>' % self.uId