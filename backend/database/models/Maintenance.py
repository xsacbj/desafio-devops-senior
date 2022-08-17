import sys
sys.path.append('../..')

from .Base import Serializer
_Maintenance = None

def createMaintenance(db):
    
    class Maintenance(db.Model, Serializer):
        __tablename__ = 'Maintenance'
        __database__ = db
        
        id = db.Column(db.Integer, primary_key= True)
        licensePlate = db.Column(db.String(45))
        timeEstimate = db.Column(db.Integer)
        status = db.Column(db.String(45))
        createAt = db.Column(db.DateTime, default=db.func.current_timestamp())

        def serialize(self):
            data = Serializer.serialize(self)
            return data
    
    global _Maintenance
    _Maintenance = Maintenance

def getMaintenance():
    global _Maintenance
    return _Maintenance