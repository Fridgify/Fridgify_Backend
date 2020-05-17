import json
import logging

from django.db import IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException, ParseError
from rest_framework.response import Response

from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.models import exceptions
from Fridgify_Backend.models import UserFridge, Fridges, FridgeSerializer
from Fridgify_Backend.utils import const
from Fridgify_Backend.utils.decorators import check_body


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
    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        logger.error(f"Couldn't parse JSON:\n {request.body.decode('utf-8')}")
        raise ParseError()
    logger.info(f"Create fridge {body['name']} for user {request.user.username}...")
    try:
        if UserFridge.objects.filter(user=request.user, fridge__name=body["name"]).exists():
            logger.warning(f"Fridge {body['name']} already exists...")
            raise exceptions.ConflictException(detail="Fridge name already exists for user")
        if "description" in body:
            logger.debug(f"fridge_name: {body['name']}, fridge_description: {body['description']}")
            fridge = Fridges.objects.create(name=body["name"], description=body["description"])
        else:
            logger.debug(f"fridge_name: {body['name']}")
            fridge = Fridges.objects.create(name=body["name"])
        logger.info("Connect user to fridge...")
        UserFridge.objects.create(user=request.user, fridge=fridge, role=const.Constants.ROLE_OWNER)
        return Response(data=FridgeSerializer(fridge).data, status=201)
    except IntegrityError:
        logger.warning(f"Integrity Error: fridge {body['name']} already exists or user-fridge combo exists")
        raise APIException(detail="Something went wrong", code=500)
