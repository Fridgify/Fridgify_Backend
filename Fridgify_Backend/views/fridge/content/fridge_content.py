import time
import json

from django.db.models import F
from django.db import IntegrityError
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from Fridgify_Backend.utils.decorators import check_body, check_fridge_access
from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.models import (
    FridgeContent,
    FridgeContentSerializer,
    Items,
    Stores,
)


keys = ("name", "buy_date", "expiration_date", "amount", "unit", "store")


@swagger_auto_schema(
    method="get",
    manual_parameters=[openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        "API-Token",
        required=True,
        type=openapi.TYPE_STRING
    )],
    operation_description="Retrieve list of contents of a fridge",
    # TODO: Schema for FridgeContent to show what is actually returned
    responses={
        200: openapi.Response("Retrieved contents", FridgeContentSerializer(many=True)),
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@swagger_auto_schema(
    method="post",
    manual_parameters=[openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        "API-Token",
        required=True,
        type=openapi.TYPE_STRING
    )],
    operation_description="Add item to a fridge",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(type=openapi.TYPE_STRING),
            "description": openapi.Schema(type=openapi.TYPE_STRING),
            "buy_date": openapi.Schema(type=openapi.TYPE_STRING, pattern="YYYY-mm-dd"),
            "expiration_date": openapi.Schema(type=openapi.TYPE_STRING, pattern="YYYY-mm-dd"),
            "amount": openapi.Schema(type=openapi.TYPE_INTEGER),
            "unit": openapi.Schema(type=openapi.TYPE_STRING),
            "store": openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={
        201: openapi.Response("Created", FridgeContentSerializer),
        500: "Item already exists",
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@api_view(["GET", "POST"])
@check_fridge_access()
@permission_classes([IsAuthenticated])
@authentication_classes([APIAuthentication])
def fridge_content_view(request, fridge_id):
    response = get_content(request, fridge_id) if request.method == "GET" else add_content(request, fridge_id)
    return response


def get_content(_, fridge_id):
    """
    Retrieve contents of a fridge
    :param _
    :param fridge_id
    :return: json of whole content of fridge
    """
    contents = FridgeContent.objects.filter(fridge_id=fridge_id).values(
        "item_id",
        "expiration_date",
        "amount",
        "unit",
        name=F("item__name"),
    )

    for content in contents:
        content["expiration_date"] = content["expiration_date"].strftime("%Y-%m-%d")

    return Response(data=contents, status=200)


@check_body(*keys)
def add_content(request, fridge_id):
    """
    Add item to a fridge
    :param request
    :param fridge_id
    :return: json of created fridge
    """
    body = json.loads(request.body.decode("utf-8"))
    try:
        fridge = FridgeContent.objects.create(
            item=Items.objects.get_or_create(
                name=body["name"],
                store=Stores.objects.get_or_create(
                    name=body["store"]
                )[0],
                defaults={
                    "description": body["description"] if "description" in body else ""
                }
            )[0],
            fridge_id=fridge_id,
            amount=body["amount"],
            unit=body["unit"],
            expiration_date=timezone.datetime.strptime(body["expiration_date"], "%Y-%m-%d"),
        )
        return Response(data=FridgeContentSerializer(fridge).data, status=201)
    except IntegrityError:
        raise APIException(detail="Item already exists", code=500)
