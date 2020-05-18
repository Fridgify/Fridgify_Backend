import os
import logging

import hopper_api


class HopperMessaging:
    logger = logging.getLogger(__name__)
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        if not hasattr(self, 'api'):
            hopper_env = hopper_api.HopperDev if os.environ["ENVIRONMENT"] == "develop" else hopper_api.HopperProd
            self.api = hopper_api.HopperApi(hopper_env)
        if not hasattr(self, 'app'):
            self.app = self.api.deserialize_app(open(os.environ["HP_APP"], "r").read())

    def send_message(self, recipients, title, body, **kwargs):
        self.logger.info("Send notifications to Firebase...")
        print("Using Hopper")
        self.logger.debug(f"Title: {title}\n Body: {body}")

    def subscribe(self, callback_url):
        self.logger.info("Create subscribe request")
        return self.app.create_subscribe_request(callback_url)
