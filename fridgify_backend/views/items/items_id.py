"""Item ID related views"""
# pylint: disable=no-member

import json
import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from fridgify_backend.models.backends import APIAuthentication
from fridgify_backend.models import Items, ItemsSerializer, Stores

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
    operation_description="Retrieve an item based on its id",
    responses={
        200: openapi.Response("Retrieved item", ItemsSerializer),
        404: "Item not found",
        422: "Missing parameter item_id"
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@swagger_auto_schema(
    method="patch",
    manual_parameters=[openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        "API-Token",
        required=True,
        type=openapi.TYPE_STRING
    )],
    operation_description="Edit an item",
    responses={
        200: openapi.Response("Edited item", ItemsSerializer),
        404: "Item not found",
        422: "Missing parameter item_id"
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@api_view(["GET", "PATCH"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
def id_view(request, item_id=None):
    """Entry point for item id view"""
    if item_id is None:
        return Response(status=422, data="Missing parameter item_id")

    if request.method == "GET":
        logger.info("Get all items...")
        try:
            item = Items.objects.get(item_id=item_id)
            if item is None:
                return Response(status=404)
            return Response(status=200, data=ItemsSerializer(item).data)
        except Items.DoesNotExist:
            raise NotFound(detail="No item found")

    logger.info("Edit item %s", item_id)
    return edit_item(request, item_id)


def edit_item(request, item_id):
    """Edit item values based on body"""
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        raise ParseError(detail="Couldn't parse body")

    logger.debug("Update values: %s", ''.join(body.keys()))
    try:
        item = Items.objects.get(item_id=item_id)
        for key in body.keys():
            if key == "store":
                if isinstance(body[key], int):
                    item.store = Stores.objects.get(store_id=body[key])
                elif isinstance(body[key], str):
                    store, _ = Stores.objects.get_or_create(name=body[key])
                    item.store = store
            else:
                if hasattr(item, key):
                    setattr(item, key, body[key])
        item.save()
    except Items.DoesNotExist:
        raise NotFound(detail="No item found")
    return Response(status=200, data=ItemsSerializer(item).data)
