import logging

from fridgify_backend.utils import const
from fridgify_backend.utils.messaging import firebase, hopper


logger = logging.getLogger(__name__)


def send(recipients, title, body, **kwargs):
    logger.info("Sending Message...")
    for provider in recipients:
        if provider == const.Constants.FRY_NOTIFICATION_SERVICE:
            logger.debug("Using Firebase (Base Service)...")
            firebase.send_message(recipients[provider], title, body, **kwargs)
        elif provider == const.Constants.HP_NOTIFICATION_SERVICE:
            logger.debug("Using Hopper Service...")
            hopper.send_message(recipients[provider], title, body, **kwargs)
