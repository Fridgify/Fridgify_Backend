import logging
from collections import defaultdict

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.models import Items, ItemsSerializer

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
        404: "Item not found"
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@api_view(["GET"])
# @authentication_classes([APIAuthentication])
# @permission_classes([IsAuthenticated])
def id_view(request, item_id=None):
    logger.info("Retrieve item...")

    if item_id is None:
        return Response(status=422, data="Missing parameter item_id")

    filters = defaultdict(dict)
    if item_id:
        filters["item_id"] = item_id
    try:
        item = Items.objects.get(item_id=item_id)
        if item is None:
            return Response(status=404)
        return Response(status=200, data=ItemsSerializer(item).data)
    except Items.DoesNotExist:
        raise NotFound(detail="No item found")
