import sys 
sys.path.append('..')

from flask import request
from services.user import UserService
from utils.response import response

class UserController:
  def __init__(self, app=None):

    if(app is None):
      raise Exception('Empty application')
 
    self.UserService = UserService()
    # Selecionar Tudo
    @app.route("/users", methods=["GET"])
    def getUsers():
        
        users = self.UserService.list()

        return response(200, "users", users)

    # Selecionar Individual
    @app.route("/user/<id>", methods=["GET"])
    def getUser(id):

        user = self.UserService.findById(id)

        if(user is None):
            return response(404, "user", False, "User not found")

        return response(200, "user", user)

    # Cadastrar
    @app.route("/user", methods=["POST"])
    def postUser():
        body = request.get_json()

        try:

            user = self.UserService.create(body)
            
            del user['passwordHash']
        
            return response(201, "user", user, "User created")
        except Exception as e:
            return response(400, "error", str(e), "Error on create user")


    # Atualizar
    @app.route("/user/<id>", methods=["PUT"])
    def putUser(id):
        body = request.get_json()
        
        try:
            user = self.UserService.updateById(id, body)

            return response(200, "user", user, "User updated")
        except Exception as e:
            print('Error', e)

            return response(400, "id", id, "Error on update user")

    # Deletar
    @app.route("/user/<id>", methods=["DELETE"])
    def deleteUser(id):

        try:
            self.UserService.deleteById(id)

            return response(200, "id", id, "User deleted")
        except Exception as e:
            print('Erro', e)

            return response(400, "id", id, "Error on delete user")
