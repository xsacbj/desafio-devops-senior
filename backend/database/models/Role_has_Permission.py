import sys
sys.path.append('../..')

from .Base import Serializer
_Role_has_Permission = None

def createRole_has_Permission(db):
    
    class Role_has_Permission(db.Model, Serializer):
        __tablename__ = 'Role_has_Permission'
        __database__ = db
        
        Role_id = db.Column(db.Integer, db.ForeignKey('Role.id'), primary_key= True)
        Permission_id = db.Column(db.Integer, db.ForeignKey('Permission.id'), primary_key= True)

        def serialize(self):
            data = Serializer.serialize(self)
            return data
    
    global _Role_has_Permission
    _Role_has_Permission = Role_has_Permission

def getRole_has_Permission():
    global _Role_has_Permission
    return _Role_has_Permission