"""Error related view"""

import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response


logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method="get",
    operation_description="Error Page",
    responses={
        200: "OK"
    }
)
@api_view(["GET"])
def error(_):
    """Show an Error Page"""
    return Response(data={"detail": "Placeholder"}, status=200)
