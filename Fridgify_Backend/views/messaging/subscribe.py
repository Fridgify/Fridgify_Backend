import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, ParseError

from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.utils import const, dynamic_link
from Fridgify_Backend.utils.messaging import hopper


logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method="get",
    manual_parameters=[openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        "API-Token",
        required=True,
        type=openapi.TYPE_STRING
    ), openapi.Parameter(
        openapi.IN_QUERY,
        "service",
        required=True,
        type=openapi.TYPE_INTEGER,
        description="Get a subscription link for a service: 1 - None (Fridgify), 2 - Hopper"
    )],
    operation_description="Get a subscription link for a messaging service",
    responses={
        200: "Subscription URL requested successfully",
        400: "Missing/Invalid service parameter",

    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@api_view(["GET"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
def subscribe_view(request):
    service = request.GET.get("service")
    callback_url = ""
    if service is None:
        raise ValidationError(detail="Missing service argument")
    if not service.isnumeric():
        raise ParseError(detail="Service parameter should be numeric")
    service = int(service)
    if service == 1:
        return Response(data={"detail": "No subscription needed for Fridgify Notifications."}, status=200)
    if const.Constants.HP_NOTIFICATION_SERVICE == const.Constants.NOTIFICATION_SERVICES_DICT[service]:
        deep_link = dynamic_link.create_deep_link("/fridge", user_id=request.user.user_id)
        callback_url = dynamic_link.create_dynamic_link(deep_link)

    hp = hopper.HopperMessaging()
    subscribe_url = hp.subscribe(callback_url=callback_url)
    return Response(data={"subscribe_url": subscribe_url}, status=200)
