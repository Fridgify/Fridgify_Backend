"""Get Users related views"""
# pylint: disable=no-member

import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from fridgify_backend.models.backends import APIAuthentication
from fridgify_backend.models import UserFridge, FridgeUserSerializer
from fridgify_backend.utils.decorators import check_fridge_access


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
        200: openapi.Response("Retrieved fridge users", FridgeUserSerializer(many=True)),
        401: "Not authorized"
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@api_view(["GET"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
@check_fridge_access()
def fridge_users_view(request, fridge_id):
    """Entry point for fridge view"""
    logger.info(
        "User %s retrieves all user for fridge %d...",
        request.user.username, fridge_id
    )
    fridge_users = UserFridge.objects.filter(fridge_id=fridge_id)
    return Response(
        data=[
            FridgeUserSerializer(fridge_user).data
            for fridge_user in fridge_users
        ],
        status=200
    )
