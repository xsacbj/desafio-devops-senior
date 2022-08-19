import os
import sys 
sys.path.append('..')

from flask_http_middleware import BaseHTTPMiddleware
from utils.response import response
from services.user import UserService
from database.models.User import hasPermission
import jwt

secret = os.environ.get('SECRET', "secret")

actions = {
    "GET": "read",
    "POST": "create",
    "PUT": "update",
    "DELETE": "delete"
}

resources = {
    "users": "user",
    "user": "user",
    "maintenances": "maintenance",
    "maintenance": "maintenance",
    "services": "service",
    "service": "service",
    "roles": "role",
    "role": "role",
}

def generatePermission(method, path):
    action = actions[method]
    resource = resources[path.split('/')[1]]
    return f"{action}:{resource}"

class AuthMiddleware(BaseHTTPMiddleware):

    def __init__(self):
        super().__init__()
        self.ignore = ['/auth']

    def dispatch(self, request, call_next):
        path = request.path

        if path in self.ignore:
            return call_next(request)

        token = request.headers.get("Authorization")
        
        try:
            decode = jwt.decode(token, secret, algorithms=["HS256"])

            user =  UserService().findById(decode["id"])

            method = request.method
            
            permission = generatePermission(method, path)

            if user is None:
                raise Exception("User not found")
                
            if not hasPermission(user["Role_id"], permission):
                raise Exception("User not authorized")

            return call_next(request)
        except Exception as e:
            return response(401, "error", str(e), "Authorization failed")