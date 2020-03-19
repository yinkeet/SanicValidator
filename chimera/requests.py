from asyncio import get_event_loop
from functools import partial

from requests import request as _request


async def request(method, url, **kwargs):
    return await get_event_loop().run_in_executor(None, partial(_request, method, url, **kwargs))