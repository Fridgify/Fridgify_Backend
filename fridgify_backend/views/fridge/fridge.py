"""Fridge related views"""
# pylint: disable=no-member

import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from fridgify_backend.models.backends import APIAuthentication
from fridgify_backend.models import UserFridge
from fridgify_backend.utils import api_utils


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
    operation_description="Retrieve all fridges and its contents for a user",
    responses={
        200: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                    "description": openapi.Schema(type=openapi.TYPE_STRING),
                    "content": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "total": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "fresh": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "dueSoon": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "overDue": openapi.Schema(type=openapi.TYPE_INTEGER)
                        }
                    ),
                }
            )
        )
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@api_view(["GET"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
def fridge_view(request):
    """Entry point for fridge views"""
    logger.info("Retrieve fridges for user %s...", request.user.username)
    content = api_utils.get_content(request.user)

    payload = []

    fridges = UserFridge.objects.values(
        "fridge_id",
        "fridge__name",
        "fridge__description"
    ).filter(user=request.user).order_by("fridge_id")

    counter = 0
    for fridge in fridges:
        fridge_inst = {
            "id": fridge["fridge_id"],
            "name": fridge["fridge__name"],
            "description": fridge["fridge__description"],
            "content": {
                "total": 0,
                "fresh": 0,
                "dueSoon": 0,
                "overDue": 0
            }
        }
        if len(content) > 0 and counter < len(content):
            item = content[counter]
            if fridge["fridge_id"] == item["fridge_id"]:
                fridge_inst["content"]["total"] = item["total"]
                fridge_inst["content"]["fresh"] = item["fresh"]
                fridge_inst["content"]["dueSoon"] = item["dueSoon"]
                fridge_inst["content"]["overDue"] = item["overDue"]
            counter += 1

        payload.append(fridge_inst)

    logger.debug("Retrieved fridge content:\n%s", repr(payload))
    return Response(data=payload, status=200)
