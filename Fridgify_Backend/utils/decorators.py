import json
from functools import wraps

from rest_framework.exceptions import ParseError


def check_body(*keys):
    def decorator(func):
        @wraps(func)
        def wrapper(request=None, *args, **kwargs):
            body = request.body.decode("utf-8")
            for key in keys:
                if key not in json.loads(body):
                    raise ParseError(detail="Missing arguments")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
