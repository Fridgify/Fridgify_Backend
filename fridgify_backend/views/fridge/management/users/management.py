"""Fridge Management related views"""
# pylint: disable=no-member

import json
import logging

from django.db import IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import (
    PermissionDenied,
    ParseError,
    APIException,
    NotFound
)

from fridgify_backend.models.backends import APIAuthentication
from fridgify_backend.models import UserFridge, FridgeUserSerializer
from fridgify_backend.utils import const
from fridgify_backend.utils.decorators import (
    check_fridge_access,
    permissions,
    check_body,
    valid_role,
    disallowed_role
)


logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method="PATCH",
    manual_parameters=[openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        "API-Token",
        required=True,
        type=openapi.TYPE_STRING
    )],
    operation_description="Change a role for a member",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "role": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="Can be either Integer (0, 1, 2) or "
                            "String ('Fridge Owner', 'Fridge Overseer', 'Fridge User')"
            )
        }
    ),
    responses={
        200: openapi.Response("Updated user", FridgeUserSerializer),
        401: "Not authorized",
        403: "Forbidden"
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@swagger_auto_schema(
    method="DELETE",
    manual_parameters=[openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        "API-Token",
        required=True,
        type=openapi.TYPE_STRING
    )],
    operation_description="Remove member from fridge as Overseer/Owner",
    responses={
        200: "Deleted",
        401: "Not authorized",
        403: "Forbidden"
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@api_view(["PATCH", "DELETE"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
@permissions(const.Constants.ROLE_OWNER, const.Constants.ROLE_OVERSEER)
@check_fridge_access()
def user_role_view(request, fridge_id, user_id):
    """Entry point for user role view"""
    trigger = UserFridge.objects.filter(user=request.user, fridge_id=fridge_id).get()
    try:
        target = UserFridge.objects.filter(user__user_id=user_id, fridge_id=fridge_id).get()
    except UserFridge.DoesNotExist:
        raise NotFound(detail="Target User does not exist")

    if request.user.user_id == target.user_id:
        logger.error("%s user role called for own user", request.method)
        return Response(data={"detail": "Method not allowed on own user"}, status=409)

    if request.method == "PATCH":
        return edit_role(request, fridge_id, trigger, target)
    return delete_user(request, fridge_id, trigger, target)


@check_body("role")
@valid_role()
@disallowed_role(const.Constants.ROLE_OWNER, const.Constants.ROLE_S_OWNER)
def edit_role(request, fridge_id, trigger, target):  # pylint: disable=unused-argument
    """Edit role"""
    body = json.loads(request.body.decode("utf-8"))
    goal_role = body["role"]
    logger.info(
        "Change role to %s for user %d by user %d...",
        goal_role, target.user_id, request.user.user_id
    )

    if target.role == const.Constants.ROLE_OWNER:
        logger.error("Trigger tried to change role to Owner...")
        raise PermissionDenied(detail="Cannot change role of Fridge Owner")

    upd_role = (
        const.Constants.ROLES_S.index(goal_role)
        if isinstance(goal_role, str)
        else goal_role
    )

    try:
        logger.info("Change role to %s for %d...", upd_role, target.user.user_id)
        target.role = upd_role
        target.save()
    except IntegrityError:
        raise APIException(detail="Something went wrong while updating")

    return Response(data=FridgeUserSerializer(target).data, status=200)


def delete_user(request, fridge_id, trigger, target):  # pylint: disable=unused-argument
    """
    Remove a user from a fridge, based on your role.
    Overseers can only remove Users, while Owners can remove everybody.
    :request : -
    """
    if trigger.role != const.Constants.ROLE_OWNER:
        if (
                target.role == const.Constants.ROLE_OWNER or
                target.role == const.Constants.ROLE_OVERSEER
        ):
            raise PermissionDenied(detail="Cannot remove Owner or Overseer as Overseer")

    target.delete()

    return Response(status=200, data={"detail": "Deleted"})
