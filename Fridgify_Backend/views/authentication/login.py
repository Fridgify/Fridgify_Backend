from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from Fridgify_Backend.models.backends.user_authentication import UserAuthentication
from Fridgify_Backend.utils import token_handler


@api_view(['POST'])
@authentication_classes([UserAuthentication])
@permission_classes([IsAuthenticated])
def login_view(request):
    user = request.user
    if user.token_authentication is None:
        response = {"token": token_handler.generate_token(user.username, "Fridgify")}
    else:
        response = {"token": user.token_authentication}
    return Response(data=response, status=200)
