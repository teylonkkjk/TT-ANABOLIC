from django import template

register = template.Library()

@register.filter(name='can')
def can(user, permission_name):
    """
    Verifica se um usuário tem uma permissão específica.
    """
    app_name = 'TT_ANABOLIC' 
    
    return user.has_perm(f'{app_name}.{permission_name}')