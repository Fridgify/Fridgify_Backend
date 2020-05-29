from collections import defaultdict
import json
import logging

from django.core.exceptions import ValidationError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError, ParseError

from fridgify_backend.models.backends import APIAuthentication
from fridgify_backend.utils.decorators import check_fridge_access, check_body
from fridgify_backend.models import FridgeContent, FridgeContentSerializer, Items, Stores, FridgeContentItemSerializer


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
            "withdraw": openapi.Schema(type=openapi.TYPE_INTEGER, description="Only positive values")
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
    if request.method == "GET":
        logger.info(f"Retrieve item[{item_id}] of a fridge {fridge_id} for user {request.user.username}...")
        return get_item(request, fridge_id, item_id)
    elif request.method == "DELETE":
        logger.info(f"Delete item[{item_id}] of fridge {fridge_id} for user {request.user.username}...")
        FridgeContent.objects.filter(fridge_id=fridge_id, content_id=item_id).delete()
        return Response(status=200)
    else:
        logger.info(f"User {request.user.username} updates item {item_id} in fridge {fridge_id}...")
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
    except FridgeContent.DoesNotExist and Items.DoesNotExist:
        logger.error("Content or Item does not exist...")
        raise NotFound(detail="Item does not exist")
    payload = FridgeContentItemSerializer(item).data
    logger.debug(f"Retrieved item: \n{payload}")
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
        logger.error(f"Couldn't parse JSON:\n {request.body.decode('utf-8')}")
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
