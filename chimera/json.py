import re
from bson.json_util import object_hook
from json import JSONDecoder, JSONDecodeError

_NOT_WHITESPACE = re.compile(r'[^\s]')

def load(fp, *, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, buffer_size=1024, **kw):
    if cls is None:
        cls = JSONDecoder
    if object_hook is not None:
        kw['object_hook'] = object_hook
    if object_pairs_hook is not None:
        kw['object_pairs_hook'] = object_pairs_hook
    if parse_float is not None:
        kw['parse_float'] = parse_float
    if parse_int is not None:
        kw['parse_int'] = parse_int
    if parse_constant is not None:
        kw['parse_constant'] = parse_constant
    decoder = cls(**kw)

    output = []
    buffer = ''
    error = None
    while True:
        block = fp.read(buffer_size)
        if not block:
            break
        buffer += block
        pos = 0
        while True:
            match = _NOT_WHITESPACE.search(buffer, pos)
            if not match:
                break
            pos = match.start()
            try:
                obj, pos = decoder.raw_decode(buffer, pos)
            except JSONDecodeError as e:
                error = e
                break
            else:
                error = None
                output.append(obj)
        buffer = buffer[pos:]

    if error is not None:
        raise error # pylint: disable-msg=E0702

    return output