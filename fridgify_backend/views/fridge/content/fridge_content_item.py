"""FridgeContentItem related views"""
# pylint: disable=no-member

import json
import logging

from django.core.exceptions import ValidationError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError

from fridgify_backend.models.backends import APIAuthentication
from fridgify_backend.utils.decorators import check_fridge_access, check_body
from fridgify_backend.models import (
    FridgeContent,
    FridgeContentSerializer,
    Items,
    FridgeContentItemSerializer
)


logger = logging.getLogger(__name__)


@swagger_auto_schema(
    operation_id="fridge_content_item_read",
    method="get",
    manual_parameters=[openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        "API-Token",
        required=True,
        type=openapi.TYPE_STRING
    )],
    operation_description="Create a new item in the fridge",
    responses={
        200: openapi.Response("Created item in fridge", FridgeContentItemSerializer),
        404: "Item not found"
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@swagger_auto_schema(
    operation_id="fridge_content_item_delete",
    method="delete",
    manual_parameters=[openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        "API-Token",
        required=True,
        type=openapi.TYPE_STRING
    )],
    operation_description="Remove an item from the fridge",
    responses={
        200: "Deleted.",
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@swagger_auto_schema(
    operation_id="fridge_content_item_partial_update",
    method="patch",
    manual_parameters=[openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        "API-Token",
        required=True,
        type=openapi.TYPE_STRING
    )],
    operation_description="Change an existing item",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "withdraw": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="Only positive values"
            )
        }
    ),
    responses={
        200: openapi.Response("New value of the changed item", FridgeContentSerializer),
    },
)
@api_view(["GET", "DELETE", "PATCH"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
@check_fridge_access()
def fridge_content_item_view(request, fridge_id, item_id):
    """Entry point for fridge content item view"""
    if request.method == "GET":
        logger.info(
            "Retrieve item[%d] of a fridge %d for user %s...",
            item_id, fridge_id, request.user.username
        )
        return get_item(request, fridge_id, item_id)
    if request.method == "DELETE":
        logger.info(
            "Delete item[%d of fridge %d for user %s...",
            item_id, fridge_id, request.user.username
        )
        FridgeContent.objects.filter(fridge_id=fridge_id, content_id=item_id).delete()
        return Response(status=200)
    logger.info(
        "User %s updates item %d in fridge %d...",
        request.user.username, item_id, fridge_id
    )
    return update_item(request, fridge_id, item_id)


def get_item(_, fridge_id, item_id):
    """
    Retrieve an item of a fridge
    :param _:
    :param fridge_id: id of the fridge
    :param item_id: id of the item
    :return: response containing an item
    """
    try:
        item = FridgeContent.objects.get(
            fridge_id=fridge_id,
            content_id=item_id,
        )
        print(item.content_id)
    except FridgeContent.DoesNotExist:
        logger.error("Content does not exist...")
        raise NotFound(detail="Content does not exist")
    except Items.DoesNotExist:
        logger.error("Item does not exist...")
        raise NotFound(detail="Item does not exist")
    payload = FridgeContentItemSerializer(item).data
    logger.debug("Retrieved item: \n%s", repr(payload))
    return Response(payload, status=200)


@check_body("withdraw")
def update_item(request, fridge_id, item_id):
    """
    Update an item in a fridge with the given parameters in the request
    :param request: contains to be updated parameters
    :param fridge_id: id of the fridge
    :param item_id: id of the item to be updated
    :return: response containing updated item
    """
    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        logger.error("Couldn't parse JSON:\n %s", request.body.decode('utf-8'))
        raise ParseError()

    try:
        fridge_item = FridgeContent.objects.filter(content_id=item_id).get()
        fridge_item.amount -= body["withdraw"]
        if fridge_item.amount <= 0:
            fridge_item.delete()
            return Response(data={"detail": "Item was removed."}, status=200)
        fridge_item.save()
    except ValidationError:
        raise ParseError(detail="Item ID is not a valid UUID")

    return get_item(request, fridge_id, item_id)
