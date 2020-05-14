from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Fridgify_Backend.models import Accesstokens, UserFridge
from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.utils import const


@swagger_auto_schema(
    method="get",
    manual_parameters=[openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        "API-Token",
        required=True,
        type=openapi.TYPE_STRING
    ), openapi.Parameter(
        "token",
        openapi.IN_QUERY,
        required=True,
        type=openapi.TYPE_STRING
    )],
    operation_description="Join fridge with a dedicated token",
    responses={
        201: "Joined Fridge",
        403: "Forbidden",
        404: "Join Link not found",
        409: "Already member of fridge",
        410: "Link not valid anymore"
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@api_view(["GET"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
def join_view(request):
    token = request.GET.get("token")
    if token is None:
        raise ValidationError(detail="Missing token argument")

    try:
        token_obj = Accesstokens.objects.filter(provider__name="Fridgify-Join", accesstoken=token).get()
    except Accesstokens.DoesNotExist:
        raise NotFound(detail="Join link not found")

    if token_obj.valid_till < timezone.now():
        token_obj.delete()
        return Response(status=410, data={"detail": "Link not valid anymore. Ask a member to invite you again."})

    if UserFridge.objects.filter(user_id=request.user.user_id, fridge_id=token_obj.fridge_id).exists():
        return Response(status=409, data={"detail": "Already member of fridge"})

    UserFridge.objects.create(
        user_id=request.user.user_id,
        fridge_id=token_obj.fridge_id,
        role=const.ROLE_USER
    )

    return Response(status=201, data={"detail": "Joined Fridge successfully"})
