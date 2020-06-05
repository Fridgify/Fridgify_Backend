"""Module contains decorators"""
# pylint: disable=no-member, keyword-arg-before-vararg

import json
from functools import wraps

from rest_framework.exceptions import (
    ParseError,
    NotAuthenticated,
    NotFound,
    NotAcceptable,
    PermissionDenied
)

from fridgify_backend.models import UserFridge, Fridges
from fridgify_backend.utils import const


def check_body(*keys):
    """Check if body contains all passed keys"""
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
    """Check if user has access to the fridge"""
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
    """Check if permitted keys are in body"""
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
    """Check if user has appropriate roles"""
    def decorator(func):
        @wraps(func)
        def wrapper(request=None, fridge_id=None, *args, **kwargs):
            fridge = UserFridge.objects.get(fridge_id=fridge_id, user=request.user)
            if fridge.role not in roles:
                raise NotAuthenticated(detail="User lacks permission to perform this action")
            return func(request, fridge_id, *args, **kwargs)
        return wrapper
    return decorator


def required_either_keys(*values):
    """Request body should contain one of the given values"""
    def decorator(func):
        @wraps(func)
        def wrapper(request=None, *args, **kwargs):
            body = json.loads(request.body.decode("utf-8"))
            for value in values:
                if value in body:
                    return func(request, *args, **kwargs)
            raise ParseError(detail="Key is missing")
        return wrapper
    return decorator


def valid_role():
    """Check if given role is valid"""
    def decorator(func):
        @wraps(func)
        def wrapper(request=None, *args, **kwargs):
            body = json.loads(request.body.decode("utf-8"))
            role = body["role"]
            if role not in const.Constants.ROLES + const.Constants.ROLES_S:
                raise NotAcceptable(detail="Role does not exist")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def disallowed_role(*roles):
    """Check if given role is allowed"""
    def decorator(func):
        @wraps(func)
        def wrapper(request=None, *args, **kwargs):
            body = json.loads(request.body.decode("utf-8"))
            role = body["role"]
            for d_role in roles:
                if role == d_role:
                    raise PermissionDenied("Role not allowed")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
