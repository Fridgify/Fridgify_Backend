"""Duplicate users related views"""
# pylint: disable=no-member

import json
import logging

from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from fridgify_backend.models import Users
from fridgify_backend.utils.decorators import required_either_keys


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
                    "username": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Same value as in request"
                    ),
                    "email": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Same value as in request"
                    )
                }
            )
        )
    }
)
@api_view(["POST"])
@required_either_keys("email", "username")
def users_duplicate_view(request):
    """Entry point for duplicate user views"""
    logger.info("Check for duplicate user...")
    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        logger.error("Couldn't parse JSON:\n %s", request.body.decode('utf-8'))
        raise ParseError()

    username = body.get("username")
    email = body.get("email")

    exists = {"detail": "No duplicates"}
    status = 200

    if Users.objects.filter(email=email):
        exists["email"] = email
        status = 409
        exists.pop("detail", None)
    if Users.objects.filter(username=username):
        exists["username"] = username
        status = 409
        exists.pop("detail", None)
    logger.debug("Existing values: %s", repr(exists))

    return Response(data=exists, status=status)
