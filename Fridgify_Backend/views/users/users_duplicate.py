import json
import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from Fridgify_Backend.models import Users


logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method="post",
    operation_description="Check if your credentials are unique",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING),
            "email": openapi.Schema(type=openapi.TYPE_STRING)
        }
    ),
    responses={
        200: "No duplicates",
        409: openapi.Response(
            "Given parameters already exist",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "username": openapi.Schema(type=openapi.TYPE_STRING, description="Same value as in request"),
                    "email": openapi.Schema(type=openapi.TYPE_STRING, description="Same value as in request")
                }
            )
        )
    }
)
@api_view(["POST"])
def users_duplicate_view(request):
    logger.info("Check for duplicate user...")
    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        logger.error(f"Couldn't parse JSON:\n {request.body.decode('utf-8')}")
        raise ParseError()
    exists = {}
    for key in body.keys():
        if key == "username":
            logger.debug(f"Check for duplicate username {body[key]}...")
            if Users.objects.filter(username=body[key]).exists():
                exists["username"] = body[key]
        if key == "email":
            logger.debug(f"Check for duplicate email {body[key]}...")
            if Users.objects.filter(email=body[key]).exists():
                exists["email"] = body[key]
    logger.debug(f"Existing values: {exists}")
    if exists:
        return Response(data=exists, status=409)
    else:
        return Response(data={"detail": "No duplicates"}, status=200)