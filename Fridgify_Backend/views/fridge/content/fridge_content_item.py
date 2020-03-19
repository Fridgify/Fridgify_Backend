from collections import defaultdict
import json

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.utils.decorators import check_fridge_access, permitted_keys
from Fridgify_Backend.utils.api_utils import serialize_object
from Fridgify_Backend.models import FridgeContent, Items, Stores


@api_view(["GET", "DELETE", "PATCH"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
@check_fridge_access()
def fridge_content_item_view(request, fridge_id, item_id):
    if request.method == "GET":
        return get_item(request, fridge_id, item_id)
    elif request.method == "DELETE":
        FridgeContent.objects.filter(fridge_id=fridge_id, item_id=item_id).delete()
        return Response(status=200)
    else:
        return update_item(request, fridge_id, item_id)


def get_item(_, fridge_id, item_id):
    try:
        item = FridgeContent.objects.get(
            fridge_id=fridge_id,
            item_id=item_id,
        ).item
    except FridgeContent.DoesNotExist and Items.DoesNotExist:
        raise NotFound(detail="Item does not exist")
    return Response(serialize_object(item, True), status=200)


@permitted_keys("item_id", "store_id")
def update_item(request, fridge_id, item_id):
    body = json.loads(request.body.decode("utf-8"))
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
        FridgeContent.objects.filter(fridge_id=fridge_id, item_id=item_id).update(**update_content)
    if update_items:
        Items.objects.filter(item_id=item_id).update(**update_items)

    return get_item(request, fridge_id, item_id)
