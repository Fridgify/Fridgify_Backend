"""Messaging register related views"""
# pylint: disable=no-member

import json
import logging

from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from fridgify_backend.models import Accesstokens, Providers
from fridgify_backend.models.backends import APIAuthentication
from fridgify_backend.utils.decorators import check_body
from fridgify_backend.utils import const


logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method="post",
    operation_description="Register client token for Cloud Messaging",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "client_token": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Client token for Messaging Service"
            ),
            "service": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="1 - Fridgify (Default), 2 - Hopper",
            )
        },
        required=["client_token"],
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
    """Entry point for register messaging view"""
    body = json.loads(request.body)

    service = const.Constants.FRY_NOTIFICATION_SERVICE
    if "service" in body.keys():
        service = const.Constants.NOTIFICATION_SERVICES_DICT[body["service"]]

    logger.debug('Client-Token for Firebase Messaging: %s', body["client_token"])
    obj, _ = Accesstokens.objects.get_or_create(
        user_id=request.user.user_id,
        provider=Providers.objects.get(provider_id=service),
        accesstoken=body["client_token"],
        defaults={
            "valid_till": timezone.datetime.max
        }
    )
    return Response(
        data={"detail": "Created", "token": obj.accesstoken},
        status=201
    )
