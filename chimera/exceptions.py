from sanic.exceptions import add_status_code, SanicException, NotFound

@add_status_code(409)
class Conflict(SanicException):
    pass

class DocumentNotFound(NotFound):
    def __init__(self, field, value, document_name='document', extra=None):
        messages = ['{} \'{}\' not found'.format(document_name.capitalize(), value)]
        if isinstance(extra, str):
            messages.append(extra)
        if isinstance(extra, list):
            messages.extend(extra)
        super().__init__({
            field: messages
        })