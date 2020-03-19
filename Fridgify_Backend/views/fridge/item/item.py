from collections import defaultdict

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.models import Items


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
        Items.objects.filter(**filters)
    except Items.DoesNotExist:
        raise NotFound(detail="No item found")
