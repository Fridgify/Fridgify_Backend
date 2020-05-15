import json
import logging

from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from Fridgify_Backend.models import Accesstokens, Providers
from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.utils.decorators import check_body


logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method="post",
    operation_description="Register client token for Cloud Messaging",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "client_token": openapi.Schema(type=openapi.TYPE_STRING, description="Client token for Messaging Service")
        }
    ),
    responses={
        201: "Created"
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@api_view(["POST"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
@check_body("client_token")
def register_view(request):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        raise ParseError

    logger.debug(f'Client-Token for Firebase Messaging: {body["client_token"]}')
    obj, _ = Accesstokens.objects.get_or_create(
        user_id=request.user.user_id,
        provider=Providers.objects.get(name="Fridgify-Notifications"),
        accesstoken=body["client_token"],
        defaults={
            "valid_till": timezone.datetime.max
        }
    )
    return Response(data={"detail": "Created"}, status=201)
