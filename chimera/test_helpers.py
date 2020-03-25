from datetime import datetime

from bson import ObjectId
from cerberus import TypeDefinition
from cerberus import Validator as BaseValidator
from sanic.request import File


class MockResponse:
    def __init__(self, status_code: int, json_response: dict):
        self.status_code = status_code
        self.json_response = json_response

    @property
    def text(self):
        return ''

    def json(self, **kwargs):
        return self.json_response

class Validator(BaseValidator):
    # Types
    types_mapping = BaseValidator.types_mapping.copy()
    types_mapping['file'] = TypeDefinition('file', (File,), ())
    types_mapping['datetime'] = TypeDefinition('datetime', (datetime,), ())
    types_mapping['object_id'] = TypeDefinition('object_id', (ObjectId,), ())