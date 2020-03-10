def non_unique_keys(request_body, model, *args):
    keys = []
    for unique_key in args:
        print(unique_key)
        if model.objects.filter(**{unique_key: request_body[unique_key]}).exists():
            keys.append(unique_key)
    return keys
