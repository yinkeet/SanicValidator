from copy import deepcopy
from datetime import datetime
from typing import List, Tuple

from bson import ObjectId
from cerberus import TypeDefinition
from cerberus import Validator as BaseValidator
from sanic.request import File
from requests import Response

class MockResponse:
    def __init__(self, status_code: int, json_response: dict={}, headers: dict={}):
        self.status_code = status_code
        self.json_response = json_response
        self.headers = headers

    @property
    def content(self):
        return b''

    @property
    def text(self):
        return ''

    def json(self, **kwargs):
        return self.json_response
        
class MockResponsesFactory:
    def __init__(self, original_responses: dict):
        self.original_responses = original_responses

    def build(self, *replacements: Tuple[str, str, MockResponse]):
        responses = deepcopy(self.original_responses)
        for method, url, response in replacements:
            responses[method][url] = response
        return responses

class Validator(BaseValidator):
    # Types
    types_mapping = BaseValidator.types_mapping.copy()
    types_mapping['file'] = TypeDefinition('file', (File,), ())
    types_mapping['datetime'] = TypeDefinition('datetime', (datetime,), ())
    types_mapping['object_id'] = TypeDefinition('object_id', (ObjectId,), ())
