import json
import logging

from django.db import IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ParseError, NotAcceptable, APIException

from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.models import UserSerializer, UserFridge, Users, FridgeUserSerializer
from Fridgify_Backend.utils.decorators import check_fridge_access, permissions, check_body


logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method="get",
    manual_parameters=[openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        "API-Token",
        required=True,
        type=openapi.TYPE_STRING
    )],
    operation_description="Retrieve all users, who have access to fridge",
    responses={
        200: openapi.Response("Retrieved fridge users", UserSerializer(many=True)),
        401: "Not authorized"
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@api_view(["GET"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
@check_fridge_access()
def fridge_users_view(request, fridge_id):
    logger.info(f"User {request.user.username} retrieves all user for fridge {fridge_id}...")
    fridge_users = UserFridge.objects.filter(fridge_id=fridge_id)
    return Response(data=[FridgeUserSerializer(fridge_user).data for fridge_user in fridge_users], status=200)


@api_view(["PATCH"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
@check_body("role")
@permissions(UserFridge.OWNER, UserFridge.OVERSEER)
@check_fridge_access()
def user_role_view(request, fridge_id, user_id):
    logger.info(f"Change role for user {user_id} by user {request.user.user_id}...")
    if request.user.user_id == user_id:
        logger.error("User tried to change role for himself")
        return Response(data={"detail": "User cannot change role for himself"}, status=409)
    
    trigger = UserFridge.objects.filter(user=request.user, fridge_id=fridge_id).get()
    target = UserFridge.objects.filter(user__user_id=user_id, fridge_id=fridge_id).get()

    body = json.loads(request.body.decode("utf-8"))
    if target.role == UserFridge.OWNER:
        logger.error("Trigger tried to change role to Owner...")
        raise PermissionDenied(detail="Cannot change role of Fridge Owner")

    if (body["role"] not in UserFridge.ROLES_DICT.keys() and body["role"] not in UserFridge.ROLES_DICT.values()):
        logger.error("Role does not exist...")
        raise NotAcceptable(detail="Role does not exist")

    if body["role"] != "Fridge Owner" and body["role"] != 0:
        try:
            upd_role = UserFridge.ROLES_DICT[body["role"]] if type(body["role"]) is str else body["role"]
        except KeyError:
            raise ParseError(detail="Couldn't determine role")
        
        try:
            logger.info(f"Change role to {upd_role} for {target.user.user_id}...")
            target.role = upd_role
            target.save()
        except IntegrityError:
            raise APIException(detail="Something went wrong while updating")
    else:
        raise PermissionDenied(detail="Cannot declare a Fridge Owner")

    return Response(data=FridgeUserSerializer(target).data, status=200)
