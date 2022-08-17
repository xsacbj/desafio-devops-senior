import sys
sys.path.append('../..')

from .Base import Serializer
_Service = None

def createService(db):
    
    class Service(db.Model, Serializer):
        __tablename__ = 'Service'
        __database__ = db
        
        id = db.Column(db.Integer, primary_key= True)
        description = db.Column(db.String(100))
        time = db.Column(db.Integer)
        status = db.Column(db.String(45))
        Maintenance_id = db.Column(db.Integer, db.ForeignKey('Maintenance.id'))
        
        def serialize(self):
            data = Serializer.serialize(self)
            return data
    
    global _Service
    _Service = Service

def getService():
    global _Service
    return _Service