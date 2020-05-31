"""CreateFridge related views"""
# pylint: disable=no-member

import json
import logging

from django.db import IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException, ParseError
from rest_framework.response import Response

from fridgify_backend.models.backends import APIAuthentication
from fridgify_backend.models import exceptions
from fridgify_backend.models import UserFridge, Fridges, FridgeSerializer
from fridgify_backend.utils import const
from fridgify_backend.utils.decorators import check_body


logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method="post",
    manual_parameters=[openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        "API-Token",
        required=True,
        type=openapi.TYPE_STRING
    )],
    operation_description="Create a new fridge. User becomes a <b>Fridge Owner</b>.",
    request_body=FridgeSerializer,
    responses={
        201: openapi.Response("Created fridge", FridgeSerializer),
        500: "Internal Server Error",
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@api_view(["POST"])
@check_body("name")
@permission_classes([IsAuthenticated])
@authentication_classes([APIAuthentication])
def create_fridge_view(request):
    """Entry point for create fridge view"""
    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        logger.error("Couldn't parse JSON:\n %s", request.body.decode('utf-8'))
        raise ParseError()
    logger.info("Create fridge %s for user %s...", body['name'], request.user.username)
    try:
        if UserFridge.objects.filter(user=request.user, fridge__name=body["name"]).exists():
            logger.warning("Fridge %s already exists...", body['name'])
            raise exceptions.ConflictException(detail="Fridge name already exists for user")
        if "description" in body:
            logger.debug(
                "fridge_name: %s, fridge_description: %s",
                body['name'], body['description']
            )
            fridge = Fridges.objects.create(name=body["name"], description=body["description"])
        else:
            logger.debug("fridge_name: %s", body['name'])
            fridge = Fridges.objects.create(name=body["name"])
        logger.info("Connect user to fridge...")
        UserFridge.objects.create(user=request.user, fridge=fridge, role=const.Constants.ROLE_OWNER)
        return Response(data=FridgeSerializer(fridge).data, status=201)
    except IntegrityError:
        logger.warning("Integrity Error: fridge %s already "
                       "exists or user-fridge combo exists", body['name'])
        raise APIException(detail="Something went wrong", code=500)
