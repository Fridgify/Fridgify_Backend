"""Redirect related views"""

import logging

from django.shortcuts import redirect
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from fridgify_backend.utils import redirect_handler, const


logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method="get",
    operation_description="Redirect users accordingly to another URL",
    responses={
        200: "Redirect successful"
    }
)
@api_view(["GET"])
def redirect_view(request):
    """Entry point for redirect view"""
    if request.GET.get("messaging") == "1":
        red_url = redirect_handler.redirect_messaging(request)
    else:
        red_url = const.Constants.ERROR_URL
    return redirect(red_url)
