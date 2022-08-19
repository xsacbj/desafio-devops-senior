import os
import sys
sys.path.append('../..')

from .Base import Serializer
import bcrypt
import jwt
from services.role import RoleService
_User = None

secret = os.environ.get('SECRET', "secret")

def hasPermission(Role_id, permission):
    print(permission, flush=True)
    try:
        role = RoleService().findById(Role_id)
        if role is None:
            print(role, flush=True)
            return False
        if permission not in role['permissions']:
            return False
    except:
        return False
    return True

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

        def verifyPassword(self, password):
            return bcrypt.checkpw(password.encode('utf-8'), self.passwordHash.encode('utf-8'))
        
        def getToken(self):
            return jwt.encode({"id": self.id}, secret, algorithm='HS256')

    global _User
    _User = User

def getUser():
    global _User
    return _User