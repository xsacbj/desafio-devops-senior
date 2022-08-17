import sys
sys.path.append('../..')

from .User import createUser
from .Role import createRole
from .Permission import createPermission
from .Role_has_Permission import createRole_has_Permission
from .Maintenance import createMaintenance
from .Service import createService

from services.permission import PermissionService
from services.role import RoleService

def createModels(db):
    models = [createUser, createPermission, createRole, createRole_has_Permission, createMaintenance, createService]
    
    for model in models:
        model(db)

    # Create default permissions
    # permissionService = PermissionService()
    # permissionService.create({'name': 'create:maintenance', 'action': 'create', 'resource': 'maintenance'})
    # permissionService.create({'name': 'read:maintenance', 'action': 'read', 'resource': 'maintenance'})
    # permissionService.create({'name': 'update:maintenance', 'action': 'update', 'resource': 'maintenance'})
    # permissionService.create({'name': 'delete:maintenance', 'action': 'delete', 'resource': 'maintenance'})
    # permissionService.create({'name': 'create:service', 'action': 'create', 'resource': 'service'})
    # permissionService.create({'name': 'read:service', 'action': 'read', 'resource': 'service'})
    # permissionService.create({'name': 'update:service', 'action': 'update', 'resource': 'service'})
    # permissionService.create({'name': 'delete:service', 'action': 'delete', 'resource': 'service'})
    
    # Create default roles
    roleService = RoleService()
    roleService.create({
        'name': 'Atendente', 
        'permissions': [
            # 'create:maintenance',
            # 'read:maintenance', 
            # 'update:maintenance',
            # 'delete:maintenance',
            # 'read:service'
        ]
    })
    roleService.create({
        'name': 'Mecânico', 
        'permissions': [
            # 'read:maintenance', 
            # 'create:service',
            # 'read:service', 
            # 'update:service'
            # 'delete:service'
        ]
    })