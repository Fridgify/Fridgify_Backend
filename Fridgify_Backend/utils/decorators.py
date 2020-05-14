import json
from functools import wraps

from rest_framework.exceptions import ParseError, NotAuthenticated, NotFound

from Fridgify_Backend.models import UserFridge, Fridges


def check_body(*keys):
    def decorator(func):
        @wraps(func)
        def wrapper(request=None, *args, **kwargs):
            try:
                body = json.loads(request.body.decode("utf-8"))
                for key in keys:
                    if key not in body:
                        raise ParseError(detail="Missing arguments")
            except json.JSONDecodeError:
                raise ParseError(detail="Invalid body")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def check_fridge_access():
    def decorator(func):
        @wraps(func)
        def wrapper(request=None, fridge_id=None, *args, **kwargs):
            user = request.user
            if not Fridges.objects.filter(fridge_id=fridge_id).exists():
                raise NotFound(detail="Fridge does not exist")

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


def permissions(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(request=None, fridge_id=None, *args, **kwargs):
            fridge = UserFridge.objects.get(fridge_id=fridge_id, user=request.user)
            if fridge.role not in roles:
                raise NotAuthenticated(detail="User lacks permission to perform this action")
            return func(request, fridge_id, *args, **kwargs)
        return wrapper
    return decorator
