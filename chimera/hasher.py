from hashlib import md5 as hashlib_md5
from json import dumps, loads
from zlib import crc32 as zlib_crc32


def md5(objects):
    return hashlib_md5(dumps(objects, sort_keys=True).encode('utf-8')).hexdigest()

def crc32(dictionary: dict):
    sorted_encoded_json_string = dumps(dictionary, sort_keys=True).encode('utf-8')
    return zlib_crc32(sorted_encoded_json_string)

def crc32s(json_string: str):
    dictionary = loads(json_string)
    return crc32(dictionary)