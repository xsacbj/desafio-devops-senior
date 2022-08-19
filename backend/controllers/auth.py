import sys 
sys.path.append('..')

from flask import request
from services.auth import AuthService
from utils.response import response

class AuthController:
  def __init__(self, app=None):

    if(app is None):
      raise Exception('Empty application')
 
    self.AuthService = AuthService()
    # Autenticação
    @app.route("/auth", methods=["POST"])
    def auth():
        body = request.get_json()

        try:
          token = self.AuthService.auth(body)
          return response(200, "token", token, "User authenticated")
        except Exception as e:
          return response(400, "error", str(e), "Error on authenticate user")
    
