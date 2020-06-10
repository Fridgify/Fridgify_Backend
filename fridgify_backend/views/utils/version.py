"""Version related view"""

import logging

from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response


logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method="get",
    operation_description="Get current API version",
    responses={
        200: openapi.Response('{ "version": "1.0" }')
    }
)
@api_view(["GET"])
def version(_):
    """Check the API version"""
    return Response(data={"version": settings.API_VERSION, "path": settings.API_PATH})
