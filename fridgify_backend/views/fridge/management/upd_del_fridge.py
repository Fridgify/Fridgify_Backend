"""Update, Delete Fridge View"""
import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from fridgify_backend.views.fridge.management import edit_fridge, delete_fridge
from fridgify_backend.models import FridgeSerializer
from fridgify_backend.models.backends import APIAuthentication


logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method="patch",
    manual_parameters=[openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        "API-Token",
        required=True,
        type=openapi.TYPE_STRING
    )],
    operation_description="Update fridge attributes",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(type=openapi.TYPE_STRING),
            "description": openapi.Schema(type=openapi.TYPE_STRING)
        }
    ),
    responses={
        200: openapi.Response("Edited fridge", FridgeSerializer),
        404: "Fridge not found",
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@swagger_auto_schema(
    method="delete",
    manual_parameters=[openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        "API-Token",
        required=True,
        type=openapi.TYPE_STRING
    )],
    operation_description="Delete a fridge",
    request_body=FridgeSerializer,
    responses={
        201: "Fridge deleted"
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@api_view(["PATCH", "DELETE"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
def upd_del_fridge_view(request, fridge_id):
    """Entry point for either updating or deleting a fridge"""
    if request.method == "PATCH":
        return edit_fridge.edit_fridge_view(request, fridge_id)
    else:
        return delete_fridge.delete_fridge_view(request, fridge_id)
