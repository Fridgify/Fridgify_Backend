import json
import logging
import secrets

from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Fridgify_Backend.models import Accesstokens, Providers, Fridges
from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.utils import firebase
from Fridgify_Backend.utils.decorators import check_fridge_access


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
        "token",
        openapi.IN_QUERY,
        required=True,
        type=openapi.TYPE_STRING
    )],
    operation_description="Generate a link (with embedded deep link), which allows users to join fridges",
    responses={
        201: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "dynamic_link": openapi.Schema(type=openapi.TYPE_STRING, description="Link for users"),
                "valid_till": openapi.Schema(type=openapi.TYPE_INTEGER, description="Duration of validity")
            }
        ),
        403: "Forbidden",
        500: "Unexpected Error. Either missing Provider or Internal Parse Error"
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@api_view(["GET"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
@check_fridge_access()
def gen_code_view(request, fridge_id):
    logger.info("Generate Dynamic Link for QR-Code...")
    # Generate Token and add to Accesstoken database
    try:
        token, _ = Accesstokens.objects.get_or_create(
            provider=Providers.objects.filter(name="Fridgify-Join").get(),
            user=request.user,
            fridge=Fridges.objects.filter(fridge_id=fridge_id).get(),
            defaults={
                'accesstoken': secrets.token_hex(16),
                'valid_till': timezone.now() + timezone.timedelta(hours=12)
            }
        )
    except Providers.DoesNotExist:
        raise APIException(detail="Provider does not exist. Contact your administrator.")
    logger.debug(f"Generated token {token.accesstoken} for fridge id {token.fridge.fridge_id}")

    try:
        dynamic_link = firebase.dynamic_link.create_dynamic_link(token.accesstoken, "/fridge/management/join")
    except json.JSONDecodeError:
        raise APIException(detail="Couldn't parse response")

    token.redirect_url = dynamic_link
    token.save()

    logger.debug(f"Generated link: {dynamic_link}")
    return Response(status=201, data={"dynamic_link": dynamic_link, "validation_time": 43200})
