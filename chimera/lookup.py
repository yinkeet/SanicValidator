from asyncio import get_event_loop
from functools import partial

from sanic.log import logger
from sanic.exceptions import ServerError

import requests


async def lookup1(url, params, return_id):
    response = await get_event_loop().run_in_executor(None, partial(requests.get, 
        url=url,
        params=params
    ))

    if response.status_code != 200:
        logger.error(response.text)
        raise ServerError(['Lookup has encountered an error', url, params])

    results = response.json()['results'][0]

    return {
        'id': return_id,
        'results': results
    }
