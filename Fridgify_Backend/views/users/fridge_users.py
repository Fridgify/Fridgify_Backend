from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.models import UserSerializer, UserFridge
from Fridgify_Backend.utils.decorators import check_fridge_access


@api_view(["GET"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
@check_fridge_access()
def fridge_users_view(request, fridge_id):
    users = UserFridge.objects.values("user").filter(fridge_id=fridge_id)
    return Response(data=[UserSerializer(user).data for user in users], status=200)
