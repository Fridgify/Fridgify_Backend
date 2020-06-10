"""Hopper Messaging Module"""

import os
import logging

import hopper_api
from hopper_api.notification import Notification


hopper_env = (
    hopper_api.HopperDev if os.environ["ENVIRONMENT"] == "develop" else hopper_api.HopperProd
)
API = hopper_api.HopperApi(hopper_env)
app = API.deserialize_app(open(os.environ["HP_APP"], "r").read())
logger = logging.getLogger(__name__)


def send_message(recipients, title, body):
    """Send message to Hopper service"""
    global API  # pylint: disable=global-statement
    logger.info("Send notifications to Hopper...")
    for recipient in recipients:
        try:
            notification = API.post_notification(
                recipient,
                Notification.default(heading=title, content=body)
            )
            logger.info("Notification (%s) sent...", repr(notification))
        except ConnectionError:
            logger.error("Couldn't send notification...")
            # Not doing anything here. Should still send messages to other providers
    logger.debug("Title: %s\n Body: %s", title, body)


def subscribe(callback_url):
    """Subscribe to Hopper service"""
    logger.info("Create subscribe request")
    return app.create_subscribe_request(callback_url)
