def standardize_response(namespace, response):
    if isinstance(response, list):
        return {namespace: response}

    if not response:
        return False

    return {namespace: [response]}