"""Stores related views"""
# pylint: disable=no-member

import json
import logging

from django.db import IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ParseError

from fridgify_backend.models.backends import APIAuthentication
from fridgify_backend.utils.decorators import check_body
from fridgify_backend.models import StoresSerializer, Stores


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
    operation_description="Retrieve all stores, which currently exist",
    responses={
        200: openapi.Response("All stores", StoresSerializer(many=True))
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
    operation_description="Create a new store",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(type=openapi.TYPE_STRING)
        }
    ),
    responses={
        200: openapi.Response("All stores", StoresSerializer)
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@api_view(["GET", "POST"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
def stores_view(request):
    """Entry point for stores view"""
    if request.method == "GET":
        logger.info("User %s retrieves all stores...", request.user.username)
        stores = Stores.objects.all()
        return Response(data=[StoresSerializer(store).data for store in stores], status=200)
    return create_store(request)


@check_body("name")
def create_store(request):
    """Create a store"""
    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        logger.error("Couldn't parse JSON:\n %s", request.body.decode('utf-8'))
        raise ParseError()
    logger.info("User %s store %s", request.user.username, body['name'])
    try:
        store = Stores.objects.create(name=body["name"])
        return Response(data=StoresSerializer(store).data, status=201)
    except IntegrityError:
        logger.warning("Store %s already exists", body['name'])
        raise APIException(detail="Store already exists", code=409)
