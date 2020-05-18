import logging

from Fridgify_Backend.utils import const
from Fridgify_Backend.utils.messaging import firebase, hopper


class MessageHandler:
    logger = logging.getLogger(__name__)
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        self.firebase = firebase.FirebaseMessaging()
        self.hopper = hopper.HopperMessaging()

    def send(self, recipients, title, body, **kwargs):
        self.logger.info("Sending Message...")
        for provider in recipients:
            if provider == const.Constants.FRY_NOTIFICATION_SERVICE:
                self.logger.debug("Using Firebase (Base Service)...")
                self.firebase.send_message(recipients[provider], title, body, **kwargs)
            elif provider == const.Constants.HP_NOTIFICATION_SERVICE:
                self.logger.debug("Using Hopper Service...")
                self.hopper.send_message(recipients[provider], title, body, **kwargs)
