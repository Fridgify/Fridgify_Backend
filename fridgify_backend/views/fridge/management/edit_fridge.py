"""Edit fridge related views"""
# pylint: disable=no-member

import json
import logging

from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response

from fridgify_backend.models import Fridges, FridgeSerializer
from fridgify_backend.utils import const
from fridgify_backend.utils.decorators import permissions


logger = logging.getLogger(__name__)


@permissions(const.Constants.ROLE_OWNER)
def edit_fridge_view(request, fridge_id):
    """Entry point for edit fridge view"""
    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        logger.error("Couldn't parse JSON:\n %s", request.body.decode('utf-8'))
        raise ParseError()
    logger.info("User %s updates values for fridge %d...", request.user.username, fridge_id)
    update_values = {}
    for key in body.keys():
        if key in ("name", "description"):
            logger.debug("Key: %s, Value: %s", key, body[key])
            update_values[key] = body[key]
    Fridges.objects.filter(fridge_id=fridge_id).update(**update_values)
    try:
        fridge = Fridges.objects.get(fridge_id=fridge_id)
        return Response(data=FridgeSerializer(fridge).data, status=200)
    except Fridges.DoesNotExist:
        logger.warning("Fridge %d does not exist", fridge_id)
        raise NotFound(detail="Fridge not found")
