from asyncio import get_event_loop
from functools import partial

from sanic.log import logger
from sanic.exceptions import ServerError

import requests


async def lookup(url, params=None, json=None, return_id=None):
    response = await get_event_loop().run_in_executor(None, partial(requests.request, 'GET', url,
        params=params,
        json=json
    ))

    if response.status_code != 200:
        logger.error({
            'url': url,
            'params': params,
            'json': json
        })
        logger.error(response.text)
        raise ServerError(['Lookup has encountered an error', url])

    results = response.json()['results']
    if len(results):
        results = response.json()['results'][0]

    response = {'results': results}
    if return_id:
        response['id'] = return_id
    return response