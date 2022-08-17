import sys 
sys.path.append('..')

from flask import request
from services.service import ServiceService
from utils.response import response

class ServiceController:
  def __init__(self, app=None):

    if(app is None):
      raise Exception('Empty application')
 
    self.ServiceService = ServiceService()
    # Selecionar Tudo
    @app.route("/services", methods=["GET"])
    def getServices():

        services = self.ServiceService.list()

        return response(200, "services", services)
    
    # Selecionar Todos os serviços de uma manutenção
    @app.route("/services/<Maintenance_id>", methods=["GET"])
    def getServices():

        services = self.ServiceService.listByMaintenanceId()

        return response(200, "services", services)

    # Selecionar Individual
    @app.route("/service/<id>", methods=["GET"])
    def getService(id):

        service = self.ServiceService.findById(id)

        if(service is None):
            return response(404, "service", False, "Service not found")

        return response(200, "service", service)

    # Cadastrar
    @app.route("/service", methods=["POST"])
    def postService():
        body = request.get_json()

        try:

            service = self.ServiceService.create(body)
        
            return response(201, "service", service, "Service created")
        except Exception as e:
            return response(400, "error", str(e), "Error on create service")


    # Atualizar
    @app.route("/service/<id>", methods=["PUT"])
    def putService(id):
        body = request.get_json()
        
        try:
            service = self.ServiceService.updateById(id, body)

            return response(200, "service", service, "Service updated")
        except Exception as e:
            print('Error', e)

            return response(400, "id", id, "Error on update service")

    # Deletar
    @app.route("/service/<id>", methods=["DELETE"])
    def deleteService(id):

        try:
            service = self.ServiceService.deleteById(id)

            return response(200, "id", id, "Service deleted")
        except Exception as e:
            print('Erro', e)

            return response(400, "id", id, "Error on delete service")
