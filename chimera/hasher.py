from hashlib import md5 as md5_hasher
from json import dumps

def md5(objects):
    return md5_hasher(dumps(objects, sort_keys=True).encode('utf-8')).hexdigest()