import sys
sys.path.append('../..')

from .Base import Serializer
_User = None

def createUser(db):
    
    class User(db.Model, Serializer):
        __tablename__ = 'User'
        __database__ = db
        
        id = db.Column(db.Integer, primary_key= True)
        name = db.Column(db.String(45))
        nickname = db.Column(db.String(45))
        passwordHash = db.Column(db.String(64))
        Role_id = db.Column(db.Integer, db.ForeignKey('Role.id'))

        def serialize(self):
            data = Serializer.serialize(self)
            return data
    
    global _User
    _User = User

def getUser():
    global _User
    return _User