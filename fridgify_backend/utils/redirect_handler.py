"""Handler for redirecting users to different destinations"""

import logging
import os

from fridgify_backend.utils import dynamic_link


logger = logging.getLogger(__name__)


def redirect_messaging(request):
    """Returns a redirect url, which directs users to the app"""
    status = request.GET.get("status")
    if status == "error":
        logger.error("Subscription Error: %s", request.GET.get("error"))
        deep_link = f"{os.environ['BASE_URL']}/error"
        return dynamic_link.create_dynamic_link(deep_link)
    subscription_id = request.GET.get("id")
    deep_link = dynamic_link.create_deep_link(
        "/fridge",
        user_id=request.GET.get("user_id"),
        id=subscription_id
    )
    return dynamic_link.create_dynamic_link(deep_link)
