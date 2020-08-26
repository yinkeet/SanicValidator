from functools import wraps
from inspect import signature

from sanic.exceptions import Forbidden


class Authenticate(object):
    def __init__(self, allowed_scopes: list=[], allowed_roles: list=[]):
        self.allowed_scopes = allowed_scopes
        self.allowed_roles = allowed_roles

    def __call__(self, function):
        @wraps(function)
        async def wrapper(request, *args, **kwargs):
            if self.allowed_scopes:
                headers = dict(getattr(request, 'headers', {}))
                scopes = headers.get('scope', '').split()
                allowed = any(scope in scopes for scope in self.allowed_scopes)
                if not allowed:
                    raise Forbidden(['Insufficient scope: authorized scope is insufficient'])
            if self.allowed_roles:
                headers = dict(getattr(request, 'headers', {}))
                roles = headers.get('roles', '').split()
                allowed = any(role in roles for role in self.allowed_roles)
                if not allowed:
                    raise Forbidden(['Insufficient role: authorized role is insufficient'])
            if 'oauth' in signature(function).parameters:
                kwargs['oauth'] = {
                    'headers': {
                        'x-oauth-scopes': headers['scope'],
                        'x-accepted-oauth-scopes': ' '.join(self.allowed_scopes)
                    }
                }
            return await function(request, *args, **kwargs)

        return wrapper
