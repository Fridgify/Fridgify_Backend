"""Handling messages"""
# pylint: disable=no-member

import itertools
import logging

from fridgify_backend import models
from fridgify_backend.utils import const
from fridgify_backend.utils.messaging import firebase, hopper


logger = logging.getLogger(__name__)


def send(recipients, title, body, **kwargs):
    """Send message to different providers"""
    logger.info("Sending Message...")
    for provider in recipients:
        if provider == const.Constants.FRY_NOTIFICATION_SERVICE:
            logger.debug("Using Firebase (Base Service)...")
            firebase.send_message(recipients[provider], title, body, **kwargs)
        elif provider == const.Constants.HP_NOTIFICATION_SERVICE:
            logger.debug("Using Hopper Service...")
            hopper.send_message(recipients[provider], title, body, **kwargs)


def get_recipients(fridge_id):
    """Retrieve recipients grouped by provider"""
    users = models.UserFridge.objects.values_list("user_id").filter(fridge_id=fridge_id)
    user_ids = [user[0] for user in users]

    tokens = models.Accesstokens.objects.values_list("accesstoken", "provider_id").filter(
        user_id__in=user_ids,
        provider_id__in=const.Constants.NOTIFICATION_SERVICES
    ).order_by("provider_id")

    recipients_dict = {}
    for key, value in itertools.groupby(tokens, key=lambda entry: entry[1]):
        recipients_dict[key] = [x[0] for x in value]

    return recipients_dict
