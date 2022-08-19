import sys 
sys.path.append('..')

from database.models.Maintenance import getMaintenance

class MaintenanceService:
  def __init__(self):
    self.Maintenance = getMaintenance()

  def list(self):    
    maintenances = self.Maintenance.query.all() 

    return self.Maintenance.serialize_list(maintenances)

  def findById(self, id):
    maintenance = self.Maintenance.query.filter_by(id=id).first()

    return maintenance.serialize()
  
  def findByLicensePlate(self, licensePlate):
    maintenance = self.Maintenance.query.filter_by(licensePlate=licensePlate).first()

    return maintenance.serialize()

  def create(self, data):
    db = self.Maintenance.__database__

    maintenanceAttributes = {}
    attributes = {'licensePlate'}
    attributesMissing = ', '.join([attr for attr in attributes if attr not in data])
    
    if len(attributesMissing) > 0:
      raise Exception("Missing attribute: " + attributesMissing)

  
    for attribute in attributes:
      maintenanceAttributes[attribute] = data[attribute]

    maintenanceAttributes['status'] = 'pending'
    maintenanceAttributes['timeEstimate'] = 0

    maintenance = self.Maintenance(**maintenanceAttributes)
    db.session.add(maintenance)
    db.session.commit()
    return maintenance.serialize()
  
  def updateById(self, id, data):
    db = self.Maintenance.__database__

    maintenance = self.Maintenance.query.filter_by(id=id).first()
    
    attributes = {'licensePlate'}

    for attribute in attributes:
      if(attribute in data):
        setattr(maintenance, attribute, data[attribute])
    
    db.session.add(maintenance)
    db.session.commit()

    return maintenance.serialize()
  
  def deleteById(self, id):
    db = self.Maintenance.__database__

    maintenance = self.Maintenance.query.filter_by(id=id).first()
    
    if(maintenance is None):
      raise Exception("Maintenance not found")
    
    db.session.delete(maintenance)
    db.session.commit()

    