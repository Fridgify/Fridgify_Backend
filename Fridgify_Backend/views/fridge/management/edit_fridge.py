import json
import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response

from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.models import Fridges,FridgeSerializer
from Fridgify_Backend.utils import const
from Fridgify_Backend.utils.decorators import check_body, check_fridge_access, permissions


logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method="patch",
    manual_parameters=[openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        "API-Token",
        required=True,
        type=openapi.TYPE_STRING
    )],
    operation_description="Update fridge attributes",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(type=openapi.TYPE_STRING),
            "description": openapi.Schema(type=openapi.TYPE_STRING)
        }
    ),
    responses={
        200: openapi.Response("Edited fridge", FridgeSerializer),
        404: "Fridge not found",
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@api_view(["PATCH"])
@check_body("fridge_id")
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
@permissions(const.Constants.ROLE_OWNER)
@check_fridge_access()
def edit_fridge_view(request):
    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        logger.error(f"Couldn't parse JSON:\n {request.body.decode('utf-8')}")
        raise ParseError()
    fridge_id = body["fridge_id"]
    logger.info(f"User {request.user.username} updates values for fridge {fridge_id}...")
    update_values = {}
    for key in body.keys():
        if key in ("name", "description"):
            logger.debug(f"Key: {key}, Value: {body[key]}")
            update_values[key] = body[key]
    Fridges.objects.filter(fridge_id=fridge_id).update(**update_values)
    try:
        fridge = Fridges.objects.get(fridge_id=fridge_id)
        return Response(data=FridgeSerializer(fridge).data, status=200)
    except Fridges.DoesNotExist:
        logger.warning(f"Fridge {fridge_id} does not exist")
        raise NotFound(detail="Fridge not found")
