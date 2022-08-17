import sys 
sys.path.append('..')

from database.models.Service import getService
from database.models.Maintenance import getMaintenance

class ServiceService:
  def __init__(self):
    self.Service = getService()
    self.Maintenance = getMaintenance()

  def list(self):    
    services = self.Service.query.all()

    return self.Service.serialize_list(services)
  
  def listByMaintenanceId(self, Maintenance_id):):    
    services = self.Service.query.filter_by(Maintenance_id=Maintenance_id).all()

    return self.Service.serialize_list(services)

  def findById(self, id):
    service = self.Service.query.filter_by(id=id).first()

    return service.serialize()

  def create(self, data):
    db = self.Service.__database__

    serviceAttributes = {}
    attributes = {'description', 'time', 'Maintenance_id'}
    attributesMissing = ', '.join([attr for attr in attributes if attr not in data])
    
    if len(attributesMissing) > 0:
      raise Exception("Missing attribute: " + attributesMissing)

  
    for attribute in attributes:
      serviceAttributes[attribute] = data[attribute]

    serviceAttributes['status'] = 'pending'

    service = self.Role(**serviceAttributes)
    db.session.add(service)
    service = service.serialize()

    maintenance = self.Maintenance.query.filter_by(id=data['Maintenance_id']).first()
    maintenance.timeEstimate = maintenance.timeEstimate + service['time']
    
    db.session.add(maintenance)
    db.session.commit()
    
    return service
  
  def updateById(self, id, data):
    db = self.Service.__database__

    service = self.Service.query.filter_by(id=id).first()


    if(service is None):
      raise Exception("Service not found")
    timeDifference = 0

    if data['time'] is not None:
      timeDifference = service.time - data['time']
    
    attributes = {'description', 'time', 'status'}

    for attribute in attributes:
      if(attribute in data):
        setattr(service, attribute, data[attribute])
    
    db.session.add(service)
    
    maintenance = self.Maintenance.query.filter_by(id=service.Maintenance_id).first()
    maintenance.timeEstimate = maintenance.timeEstimate - timeDifference
    
    services = self.Service.query.filter_by(Maintenance_id=maintenance.id).all()
    services = self.Service.serialize_list(services)
    
    somePending = False
    someInProgress = False
    someDone = False
    
    for service in services:
      if service['status'] == 'pending':
        somePending = True
      if service['status'] == 'inProgress':
        inProgress = True
      if service['status'] == 'done':
        Done = True  
    
    if somePending and not someInProgress and not someDone:
      maintenance.status = 'pending'
    elif someInProgress:
      maintenance.status = 'inProgress'
    elif someDone and not somePending and not someInProgress:
      maintenance.status = 'done'

    db.session.add(maintenance)
    db.session.commit()


    return service.serialize()
  
  def deleteById(self, id):
    db = self.Service.__database__

    service = self.Service.query.filter_by(id=id).first()
    
    if(service is None):
      raise Exception("Service not found")
    
    db.session.delete(service)
    db.session.commit()

    