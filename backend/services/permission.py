import sys 
sys.path.append('..')

from database.models.Permission import getPermission
from database.models.Role_has_Permission import getRole_has_Permission

class PermissionService:
  def __init__(self):
    self.Permission = getPermission()
    self.Role_has_Permission = getRole_has_Permission()

  def list(self):    
    permissions = self.Permission.query.all()

    return self.Permission.serialize_list(permissions)

  def findById(self, id):
    permission = self.Permission.query.filter_by(id=id).first()

    return permission.serialize()

  def create(self, data):
    db = self.Permission.__database__

    permissionAttributes = {}
    attributes = {'name'}
    attributesMissing = ', '.join([attr for attr in attributes if attr not in data])
    
    if len(attributesMissing) > 0:
      raise Exception("Missing attribute: " + attributesMissing)

    permissionWithSameName = self.Permission.query.filter_by(name=data['name']).first()
    
    if(permissionWithSameName is not None):
      raise Exception("Name already in use")
    
    for attribute in attributes:
      permissionAttributes[attribute] = data[attribute]

    permission = self.Permission(**permissionAttributes)
    db.session.add(permission)
    db.session.commit()
    return permission.serialize()
  
  def updateById(self, id, data):
    db = self.Permission.__database__

    permission = self.Permission.query.filter_by(id=id).first()
    
    attributes = {'name'}

    for attribute in attributes:
      if(attribute in data):
        setattr(permission, attribute, data[attribute])
    
    db.session.add(permission)
    db.session.commit()

    return permission.serialize()
  
  def deleteById(self, id):
    db = self.Permission.__database__

    permission = self.Permission.query.filter_by(id=id).first()
    
    if(permission is None):
      raise Exception("Permission not found")
    
    db.session.delete(permission)
    db.session.commit()

    