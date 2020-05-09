import json
import logging

from django.db.models import F
from django.db import IntegrityError
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ParseError

from Fridgify_Backend.utils.decorators import check_body, check_fridge_access
from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.models import (
    FridgeContent,
    FridgeContentSerializer,
    Items,
    Stores,
)


logger = logging.getLogger(__name__)
keys = ("name", "buy_date", "expiration_date", "count", "amount", "unit", "store")


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
    responses={
        200: openapi.Response(
            "Retrieved contents",
            openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "item_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "expiration_date": openapi.Schema(type=openapi.TYPE_STRING, pattern="YYYY-mm-dd"),
                        "amount": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "unit": openapi.Schema(type=openapi.TYPE_STRING),
                        "item_name": openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            )),
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
            "count": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of times the item should be added"),
            "amount": openapi.Schema(type=openapi.TYPE_INTEGER, description="Single amount, e.g. 1 (litre)"),
            "unit": openapi.Schema(type=openapi.TYPE_STRING, description="Unit for amount, e.g. litre, kilogram, etc."),
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
    logger.info(f"Retrieve fridge content for fridge {fridge_id}...")
    contents = FridgeContent.objects.filter(fridge_id=fridge_id).values(
        "item_id",
        "expiration_date",
        "max_amount",
        "amount",
        "unit",
        name=F("item__name"),
    )

    logger.debug(f"Content for fridge {fridge_id}")
    for content in contents:
        content["expiration_date"] = content["expiration_date"].strftime("%Y-%m-%d")
        logger.debug(f"{content}")

    return Response(data=contents, status=200)


@check_body(*keys)
def add_content(request, fridge_id):
    """
    Add item to a fridge
    :param request
    :param fridge_id
    :return: json of created fridge
    """
    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        logger.error(f"Couldn't parse JSON:\n {request.body.decode('utf-8')}")
        raise ParseError()
    logger.info(f"Add content to fridge {fridge_id} for user {request.user.username}...")
    try:
        logger.info(f"Create fridge item...")
        content = []
        for i in range(body["count"]):
            item = Items.objects.get_or_create(
                name=body["name"],
                store=Stores.objects.get_or_create(
                    name=body["store"]
                )[0],
                defaults={
                    "description": body["description"] if "description" in body else ""
                }
            )[0]
            fridge_item = FridgeContent.objects.create(
                item=item,
                fridge_id=fridge_id,
                max_amount=body["amount"],
                amount=body["amount"],
                unit=body["unit"],
                expiration_date=timezone.datetime.strptime(body["expiration_date"], "%Y-%m-%d"),
            )
            content.append(fridge_item)
        payload = [FridgeContentSerializer(fridge_item).data for fridge_item in content]
        logger.debug(f"Created fridge items: \n{payload}")
        return Response(data=payload, status=201)
    except IntegrityError:
        logger.warning(
            f"Integrity Error while adding item (name={body['name']}, store={body['store']}) to fridge {fridge_id}"
        )
        raise APIException(detail="Item already exists", code=500)
