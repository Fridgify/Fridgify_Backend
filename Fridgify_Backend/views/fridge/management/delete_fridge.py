import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.models import Fridges, UserFridge, FridgeSerializer
from Fridgify_Backend.utils import const
from Fridgify_Backend.utils. decorators import check_fridge_access


logger = logging.getLogger(__name__)


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
@api_view(["DELETE"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
@check_fridge_access()
def delete_fridge_view(request, fridge_id):
    logger.info(f"Delete user {request.user.username} for fridge {fridge_id}...")
    ufridge = UserFridge.objects.get(user=request.user, fridge_id=fridge_id)
    ufridge.delete()

    # Delete the fridge, if you are the Owner
    if ufridge.role == const.ROLE_OWNER:
        logger.info(f"Owner deleted fridge {fridge_id}")
        Fridges.objects.get(fridge_id=fridge_id).delete()
    return Response(data={"detail": "User was removed from fridge"}, status=200)
