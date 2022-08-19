import sys 
sys.path.append('..')

from database.models.User import getUser

class AuthService:
  def __init__(self):
    self.User = getUser()

  def auth(self, data):    
    user = self.User.query.filter_by(nickname=data['nickname']).first()

    if user is None:
      raise Exception("User not found")

    correctPassword = user.verifyPassword(data['password'])
    if not correctPassword:
      raise Exception("Password is wrong")

    return user.getToken()


    