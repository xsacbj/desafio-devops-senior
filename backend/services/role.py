import sys 
sys.path.append('..')

from database.models.Role import getRole
from database.models.Role_has_Permission import getRole_has_Permission
from database.models.Permission import getPermission

class RoleService:
  def __init__(self):
    self.Role = getRole()
    self.Role_has_Permission = getRole_has_Permission()
    self.Permission = getPermission()

  def list(self):    
    roles = self.Role.query.all()
    roles = self.User.serialize_list(users)
    for role, index in roles:
      role['permissions'] = self.Role_has_Permission.query.filter_by(Role_id=role['id']).all()
      role['permissions'] = self.Role_has_Permission.serialize_list(role['permissions'])
      for index, role_has_permission  in enumerate(role['permissions']):
        permission = self.Permission.query.filter_by(id=role_has_permission['Permission_id']).first()
        role['permissions'][index] = permission.serialize()['name']
    return roles

  def findById(self, id):
    role = self.Role.query.filter_by(id=id).first()
    role = role.serialize()
    role['permissions'] = self.Role_has_Permission.query.filter_by(Role_id=role['id']).all()
    role['permissions'] = self.Role_has_Permission.serialize_list(role['permissions'])
    for index, role_has_permission in enumerate(role['permissions']):
      permission = self.Permission.query.filter_by(id=role_has_permission['Permission_id']).first()
      role['permissions'][index] = permission.serialize()['name']

    return role

  def create(self, data):
    db = self.Role.__database__

    roleAttributes = {}
    attributes = {'name', 'permissions'}
    attributesMissing = ', '.join([attr for attr in attributes if attr not in data])
    
    if len(attributesMissing) > 0:
      raise Exception("Missing attribute: " + attributesMissing)

    roleWithSameName = self.Role.query.filter_by(name=data['name']).first()
    
    if(roleWithSameName is not None):
      raise Exception("Name already in use")

    attributes.remove('permissions')
    
    for attribute in attributes:
      roleAttributes[attribute] = data[attribute]

    role = self.Role(**roleAttributes)
    db.session.add(role)
    db.session.commit()
    print("Roles permissions: ", data['permissions'])
    for permissionName in data['permissions']:
      permission = self.Permission.query.filter_by(name=permissionName).first()
      print("Permission: ", permission,flush=True)
      if permission is not None:
        role_has_Permission = self.Role_has_Permission(Role_id=role.id, Permission_id=permission.id)
        db.session.add(role_has_Permission)

    db.session.commit()
    role = role.serialize()
    role['permissions'] = self.Role_has_Permission.query.filter_by(Role_id=role['id']).all()
    role['permissions'] = self.Role_has_Permission.serialize_list(role['permissions'])
    
    for index, role_has_permission  in enumerate(role['permissions']):
      permission = self.Permission.query.filter_by(id=role_has_permission['Permission_id']).first()
      role['permissions'][index] = permission.serialize()['name']

    return role
  
  def updateById(self, id, data):
    db = self.Role.__database__

    role = self.Role.query.filter_by(id=id).first()
    
    attributes = {'name'}

    for attribute in attributes:
      if(attribute in data):
        setattr(role, attribute, data[attribute])
    
    db.session.add(role)

    role = role.serialize()
    role['permissions'] = self.Role_has_Permission.query.filter_by(Role_id=role['id']).all()
    role['permissions'] = self.Role_has_Permission.serialize_list(role['permissions'])

    for permission in role['permissions']:
      if permission.name not in data['permissions']:
        self.Role_has_Permission.query.filter_by(Role_id=role['id'], Permission_id=permission.id).delete()
    
    for permissionName in data['permissions']:
      if permissionName not in role['permissions'].map(lambda permission: permission.name):
        permission = self.Permission.query.filter_by(name=permissionName).first()
        if permission is not None:
          role_has_Permission = self.Role_has_Permission(Role_id=role['id'], Permission_id=permission.id)
          db.session.add(role_has_Permission)

    db.session.commit()
    
    role['permissions'] = self.Role_has_Permission.query.filter_by(Role_id=role['id']).all()
    role['permissions'] = self.Role_has_Permission.serialize_list(role['permissions'])

    for index, role_has_permission in enumerate(role['permissions']):
      permission = self.Permission.query.filter_by(id=role_has_permission['Permission_id']).first()
      role['permissions'][index] = permission.serialize()['name']

    return role
  
  def deleteById(self, id):
    db = self.Role.__database__

    role = self.Role.query.filter_by(id=id).first()
    
    if(role is None):
      raise Exception("Role not found")

    self.Role_has_Permission.query.filter_by(Role_id=role.id).delete()

    db.session.delete(role)
    db.session.commit()

    