from sanic.exceptions import add_status_code, SanicException, NotFound

@add_status_code(409)
class Conflict(SanicException):
    pass

class DocumentNotFound(NotFound):
    def __init__(self, field, value, document_name='document', extra=None):
        messages = []
        template = document_name.capitalize() + ' \'{}\' not found'
        if isinstance(value, str):
            messages.append([template.format(value)])
        if isinstance(value, list):
            messages.extend([template.format(item) for item in value])
        
        if isinstance(extra, str):
            messages.append(extra)
        if isinstance(extra, list):
            messages.extend(extra)
        super().__init__({
            field: messages
        })