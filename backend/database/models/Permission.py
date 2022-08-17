import sys
sys.path.append('../..')

from .Base import Serializer
_Permission = None

def createPermission(db):
    
    class Permission(db.Model, Serializer):
        __tablename__ = 'Permission'
        __database__ = db
        
        id = db.Column(db.Integer, primary_key= True)
        name = db.Column(db.String(45))
        action = db.Column(db.String(45))
        resource = db.Column(db.String(45))

        def serialize(self):
            data = Serializer.serialize(self)
            return data
    
    global _Permission
    _Permission = Permission

def getPermission():
    global _Permission
    return _Permission