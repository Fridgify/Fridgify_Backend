from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from Fridgify_Backend.models.backends import UserAuthentication
from Fridgify_Backend.utils import token_utils
from Fridgify_Backend.utils.decorators import check_body


@api_view(['POST'])
@check_body("username", "password")
@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
def login_view(request):
    user = request.user
    if user.token_authentication is None:
        response = {"token": token_utils.create_token(user, "Fridgify")}
    else:
        response = {"token": user.token_authentication}
    return Response(data=response, status=200)
