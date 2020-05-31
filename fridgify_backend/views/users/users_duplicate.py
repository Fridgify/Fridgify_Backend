"""Duplicate users related views"""
# pylint: disable=no-member

import json
import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from fridgify_backend.models import Users


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
def users_duplicate_view(request):
    """Entry point for duplicate user views"""
    logger.info("Check for duplicate user...")
    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        logger.error("Couldn't parse JSON:\n %s", request.body.decode('utf-8'))
        raise ParseError()
    exists = {}
    for key in body.keys():
        if key == "username":
            logger.debug("Check for duplicate username %s...", body[key])
            if Users.objects.filter(username=body[key]).exists():
                exists["username"] = body[key]
        if key == "email":
            logger.debug("Check for duplicate email %s...", body[key])
            if Users.objects.filter(email=body[key]).exists():
                exists["email"] = body[key]
    logger.debug("Existing values: %s", repr(exists))
    if exists:
        return Response(data=exists, status=409)
    return Response(data={"detail": "No duplicates"}, status=200)
