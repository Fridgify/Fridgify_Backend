from collections import defaultdict
import json
import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError

from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.utils.decorators import check_fridge_access, permitted_keys
from Fridgify_Backend.models import FridgeContent, FridgeContentSerializer, Items, Stores, ItemsSerializer


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
        200: openapi.Response("Created item in fridge", FridgeContentSerializer),
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
            "expiration_date": openapi.Schema(type=openapi.TYPE_STRING, pattern="YYYY-mm-dd"),
            "amount": openapi.Schema(type=openapi.TYPE_STRING),
            "unit": openapi.Schema(type=openapi.TYPE_STRING)
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
        FridgeContent.objects.filter(fridge_id=fridge_id, item_id=item_id).delete()
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
            item_id=item_id,
        ).item
    except FridgeContent.DoesNotExist and Items.DoesNotExist:
        logger.error("Content or Item does not exist...")
        raise NotFound(detail="Item does not exist")
    payload = ItemsSerializer(item).data
    logger.debug(f"Retrieved item: \n{payload}")
    return Response(payload, status=200)


@permitted_keys("item_id", "store_id", "id")
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
    content_mappings = {
        "buy_date": "created_at",
        "expiration_date": "expiration_date",
        "amount": "amount",
        "unit": "unit",
    }
    item_mappings = {
        "name": "name",
        "description": "description",
        "store": "store__name"
    }
    update_content = defaultdict(dict)
    update_items = defaultdict(dict)
    logger.debug(f"To be updated values: {','.join(body.keys)}")
    for key in body.keys():
        if key in content_mappings:
            update_content[content_mappings[key]] = body[key]
            continue
        if key in item_mappings:
            if key == "store":
                update_items["store_id"] = Stores.objects.values("store_id").get(name=body[key])
            else:
                update_items[item_mappings[key]] = body[key]
            continue
    if update_content:
        logger.info("Content values are being updated...")
        FridgeContent.objects.filter(fridge_id=fridge_id, item_id=item_id).update(**update_content)
    if update_items:
        logger.info("Item values are being updated...")
        Items.objects.filter(item_id=item_id).update(**update_items)

    return get_item(request, fridge_id, item_id)
