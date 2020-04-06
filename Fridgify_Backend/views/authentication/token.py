from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from Fridgify_Backend.utils import token_utils
from Fridgify_Backend.models.backends import UserAuthentication


@swagger_auto_schema(
    method="get",
    operation_description="Retrieve an API-Token to interact with Fridgify's API",
    manual_parameters=[openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        "Login-Token",
        required=True,
        type=openapi.TYPE_STRING
    )],
    responses={
        201: "Created API token. Body contains token",
    },
    security=[{'Fridgify_Basic_Auth': []}, {'Fridgify_Token_Auth': []}]
)
@api_view(["GET"])
@authentication_classes([UserAuthentication])
def token_view(request):
    api_token = token_utils.create_token(request.user, "Fridgify-API")
    return Response(data={"token": api_token, "validation_time": 3600}, status=201)
