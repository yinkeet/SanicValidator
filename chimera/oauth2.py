from functools import wraps
from inspect import signature

from sanic.exceptions import Forbidden


class Authenticate(object):
    def __init__(self, allowed_scopes: list=[], inject_header: dict={}):
        self.allowed_scopes = allowed_scopes
        self.inject_header = inject_header

    def __call__(self, function):
        @wraps(function)
        async def wrapper(request, *args, **kwargs):
            scopes = request.headers.get('scope', '').split()
            allowed = any(scope in scopes  for scope in self.allowed_scopes)
            if not allowed:
                raise Forbidden(['Insufficient scope: authorized scope is insufficient'])
            for key, value in self.inject_header.items():
                if value in signature(function).parameters:
                    kwargs[value] = request.headers.get(key)
            return await function(request, *args, **kwargs)

        return wrapper
