from functools import wraps
from inspect import signature

from sanic.exceptions import Forbidden


class Authenticate(object):
    def __init__(self, allowed_scopes: list=[]):
        self.allowed_scopes = allowed_scopes

    def __call__(self, function):
        @wraps(function)
        async def wrapper(request, *args, **kwargs):
            scopes = request.headers.get('scope', '').split()
            allowed = any(scope in scopes  for scope in self.allowed_scopes)
            if not allowed:
                raise Forbidden(['Insufficient scope: authorized scope is insufficient'])
            
            return await function(request, *args, **kwargs)

        return wrapper
