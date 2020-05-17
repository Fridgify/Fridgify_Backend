import logging

import firebase_admin
from firebase_admin import messaging

from Fridgify_Backend.utils import const


class FirebaseMessaging:
    logger = logging.getLogger(__name__)
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        if not hasattr(self, 'app'):
            print("TEST")
            self.app = firebase_admin.initialize_app()

    def send_message(self, recipients, title, body, **kwargs):
        self.logger.info("Send notifications to Firebase...")
        self.logger.debug(f"Title: {title}\n Body: {body}")
        print(kwargs)
        message = messaging.MulticastMessage(
            tokens=recipients,
            data={str(key): str(kwargs[key]) for key in kwargs},
            notification=messaging.Notification(
                title=title,
                body=body
            )
        )
        messaging.send_multicast(message)
        self.logger.info("Sending notifications successful...")
