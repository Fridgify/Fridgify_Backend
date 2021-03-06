"""Barcode related views"""
# pylint: disable=no-member

import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from fridgify_backend.models.backends import APIAuthentication
from fridgify_backend.models import Items, ItemsSerializer

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
    operation_description="Retrieve an item based on its barcode",
    responses={
        200: openapi.Response("Retrieved item", ItemsSerializer),
        404: "Item not found",
        422: "Missing parameter barcode"
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@api_view(["GET"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
def barcode_view(_, barcode=None):
    """Entry point for barcode view"""
    logger.info("Retrieve item...")
    if barcode is None:
        return Response(status=422, data="Missing parameter barcode")

    try:
        item = Items.objects.filter(barcode=barcode).first()
        if item is None:
            return Response(status=404)
        return Response(status=200, data=ItemsSerializer(item).data)
    except Items.DoesNotExist:
        raise NotFound(detail="No item found")
