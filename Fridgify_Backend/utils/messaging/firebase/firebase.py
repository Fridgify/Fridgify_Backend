import logging

import firebase_admin
from firebase_admin import messaging


app = firebase_admin.initialize_app()
logger = logging.getLogger(__name__)


def send_message(recipients, title, body, **kwargs):
    logger.info("Send notifications to Firebase...")
    logger.debug(f"Title: {title}\n Body: {body}")
    message = messaging.MulticastMessage(
        tokens=recipients,
        data={str(key): str(kwargs[key]) for key in kwargs},
        notification=messaging.Notification(
            title=title,
            body=body
        )
    )
    messaging.send_multicast(message)
    logger.info("Sending notifications successful...")
