import sys
sys.path.append('../..')

from .Base import Serializer
_Role = None

def createRole(db):
    class Role(db.Model, Serializer):
        __tablename__ = 'Role'
        __database__ = db
        
        id = db.Column(db.Integer, primary_key= True)
        name = db.Column(db.String(50))
       
        def serialize(self):
            data = Serializer.serialize(self)
            return data
    
    global _Role
    _Role = Role

def getRole():
    global _Role
    return _Role