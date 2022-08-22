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
  
  def listByMaintenanceId(self, Maintenance_id):  
    services = self.Service.query.filter_by(Maintenance_id=Maintenance_id).all()
    services = self.Service.serialize_list(services)
    for index, service in enumerate(services):
      del services[index]['Maintenance_id']
    return services

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

    service = self.Service(**serviceAttributes)
    db.session.add(service)
    db.session.commit()
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

    attributes = {'description', 'time', 'status'}

    for attribute in attributes:
      if(attribute in data):
        setattr(service, attribute, data[attribute])

    
    
    Maintenance_id = service.Maintenance_id
    db.session.add(service)
    db.session.commit()
    self.refreshMaintenance(Maintenance_id)


    return service.serialize()
  
  def deleteById(self, id):
    db = self.Service.__database__

    service = self.Service.query.filter_by(id=id).first()
    Maintenance_id = service.Maintenance_id

    if(service is None):
      raise Exception("Service not found")
    
    db.session.delete(service)
    db.session.commit()
    self.refreshMaintenance(Maintenance_id)

  def refreshMaintenance(self, Maintenance_id):
    db = self.Service.__database__

    maintenance = self.Maintenance.query.filter_by(id=Maintenance_id).first()
    
    services = self.Service.query.filter_by(Maintenance_id=maintenance.id).all()
    services = self.Service.serialize_list(services)
    
    somePending = False
    someInProgress = False
    someDone = False
    time = 0
    for s in services:
      time = time + s['time']

      if s['status'] == 'pending':
        somePending = True
      if s['status'] == 'inProgress':
        someInProgress = True
      if s['status'] == 'done':
        someDone = True  

    maintenance.timeEstimate = time
    
    if somePending and not someInProgress and not someDone:
      maintenance.status = 'pending'
    elif someInProgress or (someDone and somePending):
      maintenance.status = 'inProgress'
    elif someDone and not somePending and not someInProgress:
      maintenance.status = 'done'



    db.session.add(maintenance)
    db.session.commit()



    