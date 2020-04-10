from django.db.models import Count, Case, When, IntegerField, Q
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.models import FridgeContent, UserFridge


@swagger_auto_schema(
    method="get",
    manual_parameters=[openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        "API-Token",
        required=True,
        type=openapi.TYPE_STRING
    )],
    operation_description="Retrieve all fridges and its contents for a user",
    responses={
        200: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                    "description": openapi.Schema(type=openapi.TYPE_STRING),
                    "content": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "total": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "fresh": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "dueSoon": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "overDue": openapi.Schema(type=openapi.TYPE_INTEGER)
                        }
                    ),
                }
            )
        )
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@api_view(["GET"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
def fridge_view(request):
    content = FridgeContent.objects.values(
        "fridge_id",
    ).annotate(
        total=Count("item_id"),
        fresh=Count(Case(
            When(expiration_date__gt=timezone.now() + timezone.timedelta(5), then=1),
            output_field=IntegerField()
        )),
        dueSoon=Count(Case(
            When(
                Q(expiration_date__gte=timezone.now()) & Q(expiration_date__lte=timezone.now() + timezone.timedelta(5)),
                then=1
            ),
            output_field=IntegerField()
        )),
        overDue=Count(Case(
            When(expiration_date__lt=timezone.now(), then=1),
            output_field=IntegerField()
        )),
    ).filter(fridge__userfridge__user=request.user).order_by("fridge_id")

    # TODO: If we can change the structure slightly to be flat, we do not need the for loop
    payload = []

    fridges = UserFridge.objects.values(
        "fridge_id",
        "fridge__name",
        "fridge__description"
    ).filter(user=request.user).order_by("fridge_id")

    c = 0
    for fridge in fridges:
        fridge_inst = {
            "id": fridge["fridge_id"],
            "name": fridge["fridge__name"],
            "description": fridge["fridge__description"],
            "content": {
                "total": 0,
                "fresh": 0,
                "dueSoon": 0,
                "overDue": 0
            }
        }
        if len(content) > 0:
            item = content[c]
            if fridge["fridge_id"] == item["fridge_id"]:
                fridge_inst["content"]["total"] = item["total"]
                fridge_inst["content"]["fresh"] = item["fresh"]
                fridge_inst["content"]["dueSoon"] = item["dueSoon"]
                fridge_inst["content"]["overDue"] = item["overDue"]
                c += 1

        payload.append(fridge_inst)

    return Response(data=payload, status=200)
