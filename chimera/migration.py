from typing import List, Tuple

from requests import get
from tempfile import TemporaryFile

class SanicFiles(object):
    def __init__(self, maps: List[Tuple[str, List[Tuple[str, str, str]]]]):
        self.maps = maps

    def __enter__(self):
        self.files = [(name, (url, self._prepare_temporary_file(url, suffix), content_type)) for name, configs in self.maps for url, suffix, content_type in configs]
        return self.files

    def __exit__(self, exception_type, exception_value, traceback):
        for _, f in self.files:
            f[1].close()

    def _prepare_temporary_file(self, url, suffix):
        response = get(url, stream=True)
        f = TemporaryFile(suffix=suffix)
        f.write(response.content)
        f.seek(0)
        return f
