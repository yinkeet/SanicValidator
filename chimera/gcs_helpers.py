from asyncio import get_event_loop
from functools import partial

from bson import ObjectId
from six import binary_type


def upload_file(bucket, destination, data, content_type):
    blob = bucket.blob(destination)
    blob.upload_from_string(data, content_type=content_type)

    url = blob.public_url
    if isinstance(url, binary_type):
        url = url.decode('utf-8')

    return url

async def upload_sanic_request_file(bucket, destination, image):
    return await get_event_loop().run_in_executor(None, partial(upload_file,
        bucket=bucket,
        destination=destination,
        data=image.body,
        content_type=image.type
    ))

async def delete_files(paths, bucket):
    if not paths:
        return

    # Ignore 404 errors on delete.
    await get_event_loop().run_in_executor(None, partial(bucket.delete_blobs,
        blobs=paths,
        on_error=lambda blob: None
    ))
