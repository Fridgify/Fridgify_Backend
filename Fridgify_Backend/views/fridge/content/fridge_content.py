import json

from django.db.models import F
from django.db import IntegrityError
from django.utils import timezone
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from Fridgify_Backend.utils.decorators import check_body, check_fridge_access
from Fridgify_Backend.utils.api_utils import serialize_object
from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.models import (
    FridgeContent,
    Items,
    Stores,
)


keys = ("name", "description", "buy_date", "expiration_date", "amount", "unit", "store")


@api_view(["GET", "POST"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
@check_fridge_access()
def fridge_content_view(request, fridge_id):
    response = get_content(request, fridge_id) if request.method == "GET" else add_content(request, fridge_id)
    return response


def get_content(_, fridge_id):
    contents = FridgeContent.objects.filter(fridge_id=fridge_id).values(
        "item_id",
        "expiration_date",
        "amount",
        "unit",
        name=F("item__name"),
    )
    return Response(data=contents, status=200)


@check_body(*keys)
def add_content(request, fridge_id):
    body = json.loads(request.body.decode("utf-8"))
    try:
        fridge = FridgeContent.objects.create(
            item=Items.objects.get_or_create(
                name=body["name"],
                store=Stores.objects.get_or_create(
                    name=body["store"]
                )[0],
                defaults={
                    "description": body["description"]
                }
            )[0],
            fridge_id=fridge_id,
            amount=body["amount"],
            unit=body["unit"],
            expiration_date=timezone.datetime.strptime(body["expiration_date"], "%Y-%m-%d"),
        )
        serialized = serialize_object(fridge, True)
        return Response(data=serialized, status=201)
    except IntegrityError:
        raise APIException(detail="Item already exists", code=500)
