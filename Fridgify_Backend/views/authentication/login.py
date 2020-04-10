from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from Fridgify_Backend.models.backends import UserAuthentication
from Fridgify_Backend.utils import token_utils


@swagger_auto_schema(
    method="post",
    operation_description="Login via a Login-Token or via credentials. Successful login returns a Login-Token.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING),
            "password": openapi.Schema(type=openapi.TYPE_STRING)
        },
        required=["username", "password"]
    ),
    manual_parameters=[
        openapi.Parameter("Authorization", openapi.IN_HEADER, "Login-Token", required=False, type=openapi.TYPE_STRING),
    ],
    responses={
        200: 'Authenticated. Returns token.',
        401: 'Unauthorized. Invalid credentials or token'
    },
    security=[{'Fridgify_Basic_Auth': []}, {'Fridgify_Token_Auth': []}]
)
@api_view(['POST'])
@authentication_classes([UserAuthentication])
def login_view(request):
    user = request.user
    if user.token_authentication is None:
        response = {"token": token_utils.create_token(user, "Fridgify")}
    else:
        response = {"token": user.token_authentication}
    return Response(data=response, status=200)
