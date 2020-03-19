from datetime import datetime

from bson import ObjectId
from cerberus import Validator as BaseValidator


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
    def _validate_type_object_id(self, value):
        return isinstance(value, ObjectId)

    def _validate_type_datetime(self, value):
        return isinstance(value, datetime)
