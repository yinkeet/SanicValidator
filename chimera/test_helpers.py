class MockResponse:
    def __init__(self, status_code: int, json_response: dict):
        self.status_code = status_code
        self.json_response = json_response

    def text(self):
        return ''

    def json(self, **kwargs):
        return self.json_response