ROLEPERMISSIONS_MODULE = 'TT_ANABOLIC.roles'
from rolepermissions.roles import AbstractUserRole

class Administrador(AbstractUserRole):
    available_permissions = {
        'cadastrar_produto': True,
        'editar_produto': True,
        'remover_produto': True,
    }

class Cliente(AbstractUserRole):
    available_permissions = {} 