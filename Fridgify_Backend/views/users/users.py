import json

import bcrypt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.models import UserSerializer, Users


@swagger_auto_schema(
    method="get",
    manual_parameters=[openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        "API-Token",
        required=True,
        type=openapi.TYPE_STRING
    )],
    operation_description="Retrieve information for current user",
    responses={
        200: openapi.Response("Retrieved current user", UserSerializer),
        401: "Not authorized"
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@swagger_auto_schema(
    method="patch",
    manual_parameters=[openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        "API-Token",
        required=True,
        type=openapi.TYPE_STRING
    )],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
            "email": openapi.Schema(type=openapi.TYPE_STRING),
            "name": openapi.Schema(type=openapi.TYPE_STRING),
            "surname": openapi.Schema(type=openapi.TYPE_STRING),
            "birth_date": openapi.Schema(type=openapi.TYPE_STRING, pattern="YYYY-mm-dd")
        }
    ),
    operation_description="Update information for current user",
    responses={
        201: openapi.Response("User updated", UserSerializer),
        401: "Not authorized",
        409: "Already exists"
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@api_view(["GET", "PATCH"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
def users_view(request):
    if request.method == "GET":
        return Response(data=UserSerializer(request.user).data, status=200)
    else:
        return edit_user(request)


def edit_user(request):
    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        raise ParseError()

    user = request.user
    for key in body.keys():
        if key == "username" or key == "email":
            if not Users.objects.filter(username=body[key]).exists():
                setattr(user, key, body[key])
            else:
                return Response(data={"detail": f"{key} {body[key]} already exists"}, status=409)
        elif key == "password":
            password = bcrypt.hashpw(body[key].encode("utf-8"), bcrypt.gensalt())
            user.password = password.decode("utf-8")
        else:
            if hasattr(user, key):
                setattr(user, key, body[key])
    user.save()
    return Response(data=UserSerializer(user).data, status=200)
