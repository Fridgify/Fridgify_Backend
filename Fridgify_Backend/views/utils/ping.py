import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response


logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method="get",
    operation_description="Check API status",
    responses={
        200: openapi.Response("Pong")
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@api_view(["GET"])
def ping(request):
    logger.info("Check API status...")
    return Response(data={"detail": "Pong"}, status=200)
