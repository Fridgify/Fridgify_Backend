import os
import logging

import hopper_api
from hopper_api.notification import Notification


hopper_env = hopper_api.HopperDev if os.environ["ENVIRONMENT"] == "develop" else hopper_api.HopperProd
api = hopper_api.HopperApi(hopper_env)
app = api.deserialize_app(open(os.environ["HP_APP"], "r").read())
logger = logging.getLogger(__name__)


def send_message(recipients, title, body, **kwargs):
    global api
    logger.info("Send notifications to Firebase...")
    for recipient in recipients:
        try:
            notification = api.post_notification(recipient, Notification.default(heading=title, content=body))
            logger.info(f"Notification ({notification}) sent...")
        except ConnectionError:
            logger.error("Couldn't send notification...")
            pass
    logger.debug(f"Title: {title}\n Body: {body}")


def subscribe(callback_url):
    logger.info("Create subscribe request")
    return app.create_subscribe_request(callback_url)
