from controllers.user import UserController
from controllers.auth import AuthController
from controllers.maintenance import MaintenanceController
from controllers.service import ServiceController

def setupRouters(app):
  UserController(app)
  AuthController(app)
  MaintenanceController(app)
  ServiceController(app)