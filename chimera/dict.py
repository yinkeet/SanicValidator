from collections import MutableMapping

def flatten(d, parent_key='', seperator='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + seperator + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten(v, new_key, seperator=seperator).items())
        else:
            items.append((new_key, v))
    return dict(items)