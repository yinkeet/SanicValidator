def standardize_response(namespace, response):
    if isinstance(response, list):
        return {namespace: response}

    return {namespace: [response]}