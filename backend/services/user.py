import sys 
sys.path.append('..')

from database.models.User import getUser
import bcrypt

class UserService:
  def __init__(self):
    self.User = getUser()

  def list(self):    
    users = self.User.query.all()
    users = self.User.serialize_list(users)

    return users

  def findById(self, id):
    user = self.User.query.filter_by(id=id).first()
    user = user.serialize()

    return user

  def create(self, data):
    db = self.User.__database__

    userAttributes = {}
    attributes = {'name', 'nickname', 'password', 'Role_id'}
    attributesMissing = ', '.join([attr for attr in attributes if attr not in data])
    
    if len(attributesMissing) > 0:
      raise Exception("Missing attribute: " + attributesMissing)
    attributes.remove('password')

    userWithSameNickname = self.User.query.filter_by(nickname=data['nickname']).first()
    
    if(userWithSameNickname is not None):
      raise Exception("Nickname already in use")

    userAttributes['passwordHash'] = bcrypt.hashpw(
      data['password'].encode('utf-8'), 
      bcrypt.gensalt()
    ).decode('utf-8')

    for attribute in attributes:
      userAttributes[attribute] = data[attribute]

    user = self.User(**userAttributes)
    db.session.add(user)
    db.session.commit()

    return user.serialize()
  def updateById(self, id, data):
    db = self.User.__database__

    user = self.User.query.filter_by(id=id).first()
    
    attributes = {'name', 'nickname', 'Role_id'}

    userWithSameNickname = self.User.query.filter_by(nickname=data['nickname']).first()
    
    if(userWithSameNickname is not None):
      raise Exception("Nickname already in use")

    for attribute in attributes:
      if(attribute in data):
        setattr(user, attribute, data[attribute])
    
    db.session.add(user)
    db.session.commit()

    return user.serialize()
  
  def deleteById(self, id):
    db = self.User.__database__

    user = self.User.query.filter_by(id=id).first()
    
    if(user is None):
      raise Exception("User not found")

    db.session.delete(user)
    db.session.commit()

    