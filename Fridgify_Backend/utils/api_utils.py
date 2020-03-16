from django.db import models


def non_unique_keys(request_body, model, *args):
    keys = []
    for unique_key in args:
        print(unique_key)
        if model.objects.filter(**{unique_key: request_body[unique_key]}).exists():
            keys.append(unique_key)
    return keys


def serialize_object(obj, flat=False, *args):
    if not args:
        args = obj.__dir__()
    serialized = {}
    for key in args:
        try:
            attr = getattr(obj, key)
            if isinstance(attr, models.Model):
                if flat:
                    s_obj = serialize_object(attr, flat)
                    for s_key in s_obj:
                        serialized[key + "-" + s_key] = s_obj[s_key]
                else:
                    serialized[key] = serialize_object(attr, flat, *args)
            else:
                serialized[key] = attr
        except AttributeError:
            pass
    return serialized
