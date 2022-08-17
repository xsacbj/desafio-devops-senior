import sys 
sys.path.append('..')

from flask import request
from services.maintenance import MaintenanceService
from utils.response import response

class MaintenanceController:
  def __init__(self, app=None):

    if(app is None):
      raise Exception('Empty application')
 
    self.MaintenanceService = MaintenanceService()
    # Selecionar Tudo
    @app.route("/maintenances", methods=["GET"])
    def getMaintenances():

        maintenances = self.MaintenanceService.list()

        return response(200, "maintenances", maintenances)

    # Selecionar Individual
    @app.route("/maintenance/<id>", methods=["GET"])
    def getMaintenance(id):

        maintenance = self.MaintenanceService.findById(id)

        if(maintenance is None):
            return response(404, "maintenance", False, "Maintenance not found")

        return response(200, "maintenance", maintenance)
    # Selecionar Individual por placa
    @app.route("/maintenance/plate/<licensePlate>", methods=["GET"])
    def getMaintenanceByLicensePlate(licensePlate):
            
        maintenance = self.MaintenanceService.findByLicensePlate(licensePlate)

        if(maintenance is None):
            return response(404, "maintenance", False, "Maintenance not found")

        return response(200, "maintenance", maintenance)

    # Cadastrar
    @app.route("/maintenance", methods=["POST"])
    def postMaintenance():
        body = request.get_json()

        try:

            maintenance = self.MaintenanceService.create(body)
        
            return response(201, "maintenance", maintenance, "Maintenance created")
        except Exception as e:
            return response(400, "error", str(e), "Error on create maintenance")


    # Atualizar
    @app.route("/maintenance/<id>", methods=["PUT"])
    def putMaintenance(id):
        body = request.get_json()
        
        try:
            maintenance = self.MaintenanceService.updateById(id, body)

            return response(200, "maintenance", maintenance, "Maintenance updated")
        except Exception as e:
            print('Error', e)

            return response(400, "id", id, "Error on update maintenance")

    # Deletar
    @app.route("/maintenance/<id>", methods=["DELETE"])
    def deleteMaintenance(id):

        try:
            self.MaintenanceService.deleteById(id)

            return response(200, "id", id, "Maintenance deleted")
        except Exception as e:
            print('Erro', e)

            return response(400, "id", id, "Error on delete maintenance")
