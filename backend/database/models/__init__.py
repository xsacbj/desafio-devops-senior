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
from services.user import UserService

def createModels(db):
    models = [createUser, createPermission, createRole, createRole_has_Permission, createMaintenance, createService]
    
    for model in models:
        model(db)
    db.create_all()
    db.session.commit()

    # Create default permissions
    permissionService = PermissionService()
    permissions = [
        {'name': 'create:maintenance' },
        {'name': 'read:maintenance' },
        {'name': 'update:maintenance' },
        {'name': 'delete:maintenance'},
        {'name': 'create:service'},
        {'name': 'read:service'},
        {'name': 'update:service'},
        {'name': 'delete:service'},
        {'name': 'delete:service'},
        {'name': 'create:role'},
        {'name': 'read:role'},
        {'name': 'update:role'},
        {'name': 'delete:role'},
        {'name': 'create:user'},
        {'name': 'read:user'},
        {'name': 'update:user'},
        {'name': 'delete:user'},
    ]
    for permission in permissions:
        try:
            permissionService.create(permission)
        except Exception as e:
            continue
    # Create default roles
    roleService = RoleService()
    roles = [
        {
            'name': 'Atendente', 
            'permissions': [
                'create:maintenance',
                'read:maintenance', 
                'update:maintenance',
                'delete:maintenance',
                'read:service'
            ]
        },
        {
            'name': 'Mecânico', 
            'permissions': [
                'read:maintenance', 
                'create:service',
                'read:service', 
                'update:service',
                'delete:service'
            ]
        },
        {
            'name': 'Administrador',
            'permissions': [
                'create:maintenance',
                'read:maintenance',
                'update:maintenance',
                'delete:maintenance',
                'create:service',
                'read:service',
                'update:service',
                'delete:service',
                'create:role',
                'read:role',
                'update:role',
                'delete:role',
                'create:user',
                'read:user',
                'update:user',
                'delete:user'
            ]
        }
    ]

    for role in roles:
        try:
            roleService.create(role)
        except Exception as e:
            continue

    # Create default user
    userService = UserService()
    users = [
        {
            'name': 'admin',
            'nickname': 'admin',
            'password': 'admin',
            'Role_id': 3
        },
        {
            'name': 'atendente',
            'nickname': 'atendente',
            'password': 'atendente',
            'Role_id': 1
        },
        {
            'name': 'mecanico',
            'nickname': 'mecanico',
            'password': 'mecanico',
            'Role_id': 2
        }
    ]

    for user in users:
        try:
            userService.create(user)
        except Exception as e:
            continue
