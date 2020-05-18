from sanic.log import logger
from typing import Tuple

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

def create_group_query(*fields: Tuple[str, str, bool]):
    return [
        {'$group': {
            **{'_id': None},
            **{group: {'$addToSet': {'$toString': '$' + field} if to_string else '$' + field} for group, field, to_string in fields}
        }},
        {'$project': {
            '_id': 0
        }},
    ]

def create_facet_extract_query(field, subfield, value_if_field_is_empty=None):
    field = '$' + field
    return {'$cond': [
        {'$gt': [{'$size': field}, 0]},
        {'$let': {
            'vars': {'temp': {'$arrayElemAt': [field, 0]}},
            'in': '$$temp.' + subfield
        }},
        field if value_if_field_is_empty is None else value_if_field_is_empty
    ]}

def create_to_strings_query(field):
    return {
        '$map': {
            'input': '$' + field,
            'as': 'temp',
            'in': {'$toString': '$$temp'}
        }
    }

def create_to_long_query(dest_field, source_field, remove_field_if_empty_query=False, double_reference=False):
    source_field = ('$$' if double_reference else '$') + source_field
    if remove_field_if_empty_query:
        return {
            dest_field: {'$cond': [
                {'$gt': [source_field, 0]},
                {'$toLong': source_field},
                '$$REMOVE'
            ]}
        }
    else:
        return {dest_field: {'$toLong': source_field}}

async def custom_aggregate(collection, query, function_name=None, session=None, to_list=False):
    if function_name:
        logger.debug('%s query %s', function_name, query)
    
    cursor = collection.aggregate(query, session=session)
    if to_list:
        output = await cursor.to_list(None)
    else:
        output = await cursor.fetch_next
        output = cursor.next_object()

    if function_name:
        logger.debug('%s response %s', function_name, output)

    return output

def remove_field_if_empty_query(field):
    ref_field = '$' + field
    return {'$cond': [{'$gt': [{'$size': ref_field}, 0]}, ref_field, '$$REMOVE']}