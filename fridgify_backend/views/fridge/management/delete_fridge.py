"""Delete Fridge related views"""
# pylint: disable=no-member

import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from fridgify_backend.models.backends import APIAuthentication
from fridgify_backend.models import Fridges, UserFridge, FridgeSerializer
from fridgify_backend.utils import const
from fridgify_backend.utils. decorators import check_fridge_access


logger = logging.getLogger(__name__)


@check_fridge_access()
def delete_fridge_view(request, fridge_id):
    """Entry point for delete fridge view"""
    logger.info("Delete user %s for fridge %d...", request.user.username, fridge_id)
    u_fridge = UserFridge.objects.get(user=request.user, fridge_id=fridge_id)
    u_fridge.delete()

    # Delete the fridge, if you are the Owner
    if u_fridge.role == const.Constants.ROLE_OWNER:
        logger.info("Owner deleted fridge %d", fridge_id)
        Fridges.objects.get(fridge_id=fridge_id).delete()
    return Response(data={"detail": "User was removed from fridge"}, status=200)
