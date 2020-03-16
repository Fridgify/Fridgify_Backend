import json
from functools import wraps

from rest_framework.exceptions import ParseError, NotAuthenticated

from Fridgify_Backend.models import UserFridge


def check_body(*keys):
    def decorator(func):
        @wraps(func)
        def wrapper(request=None, *args, **kwargs):
            body = json.loads(request.body.decode("utf-8"))
            for key in keys:
                if key not in body:
                    raise ParseError(detail="Missing arguments")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def check_fridge_access():
    def decorator(func):
        @wraps(func)
        def wrapper(request=None, fridge_id=None, *args, **kwargs):
            user = request.user
            if UserFridge.objects.filter(fridge_id=fridge_id, user=user).exists():
                return func(request, fridge_id, *args, **kwargs)
            raise NotAuthenticated(detail="No access to fridge")
        return wrapper
    return decorator


def permitted_keys(*keys):
    def decorator(func):
        @wraps(func)
        def wrapper(request=None, *args, **kwargs):
            body = json.loads(request.body.decode("utf-8"))
            invalid_keys = []
            for key in keys:
                if key in body:
                    invalid_keys.append(key)
            if invalid_keys:
                raise ParseError(detail=f"{', '.join(invalid_keys)} are not permitted")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
