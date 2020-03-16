from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Fridgify_Backend.utils import token_utils
from Fridgify_Backend.models.backends import UserAuthentication


@api_view(["GET"])
@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
def token_view(request):
    api_token = token_utils.create_token(request.user, "Fridgify-API")
    return Response(data={"token": api_token, "validation_time": 3600}, status=201)
