from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from Fridgify_Backend.models.backends import UserAuthentication
from Fridgify_Backend.utils import token_utils


@api_view(['POST'])
@authentication_classes([UserAuthentication])
def login_view(request):
    user = request.user
    if user.token_authentication is None:
        response = {"token": token_utils.create_token(user, "Fridgify")}
    else:
        response = {"token": user.token_authentication}
    return Response(data=response, status=200)
