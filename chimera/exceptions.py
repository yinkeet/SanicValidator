from sanic.exceptions import add_status_code, SanicException

@add_status_code(409)
class Conflict(SanicException):
    pass