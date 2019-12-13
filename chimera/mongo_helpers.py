from sanic.log import logger

def create_sort_query(fields):
    """Creates a sort query for mongo aggregation"""
    results=[]
    marker = set()

    for field in fields:
        lowercased_value = field.lower()
        if lowercased_value not in marker:
            marker.add(lowercased_value)
            results.append(field)

    return { (field.lower()):(1 if field.isupper() else -1) for field in results }

async def custom_aggregate(collection, query, function_name=None):
    if function_name:
        logger.debug('%s query %s', function_name, query)
    
    cursor = collection.aggregate(query)
    output = await cursor.fetch_next
    output = cursor.next_object()

    if function_name:
        logger.debug('%s response %s', function_name, output)

    return output