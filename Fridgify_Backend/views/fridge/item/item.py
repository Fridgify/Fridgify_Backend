from collections import defaultdict

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.models import Items, ItemsSerializer


@swagger_auto_schema(
    method="get",
    manual_parameters=[openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        "API-Token",
        required=True,
        type=openapi.TYPE_STRING
    )],
    operation_description="Retrieve an item based on its barcode or item id",
    responses={
        200: openapi.Response("Retrieved item", ItemsSerializer),
        404: "Item not found"
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@api_view(["GET"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
def item_view(request, barcode=None, item_id=None):
    filters = defaultdict(dict)
    if item_id:
        filters["item_id"] = item_id
    if barcode:
        filters["barcode"] = barcode
    try:
        items = Items.objects.filter(**filters)
        return Response(status=200, data=ItemsSerializer(items).data)
    except Items.DoesNotExist:
        raise NotFound(detail="No item found")
