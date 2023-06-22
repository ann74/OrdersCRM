from django.http import HttpRequest


def get_user_role(request: HttpRequest) -> str:
    if request.user.groups.first().name == 'clients':
        role = 'client'
    elif request.user.groups.first().name == 'masters':
        role = 'master'
    else:
        role = 'dispatcher'
    return role
