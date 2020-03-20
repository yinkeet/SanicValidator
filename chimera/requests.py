from asyncio import get_event_loop
from functools import partial

import requests


async def request(method, url, **kwargs):
    return await get_event_loop().run_in_executor(None, partial(requests.request, method, url, **kwargs))