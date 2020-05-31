"""Test file for Message Handler"""

from django.test import TestCase

from fridgify_backend.utils.messaging import message_handler
from fridgify_backend.tests import test_utils


class TestCaseMessageHandler(TestCase):
    """TestCase for message handling"""
    fixtures = [
        "fridgify_backend/fixtures/providers.json",
        "fridgify_backend/tests/fixtures/stores.json"
    ]

    def setUp(self) -> None:
        """Setup for test case"""
        self.user = test_utils.create_dummyuser()
        self.user_b = test_utils.create_dummyuser(username="User B", email="b@d.de")
        self.fridge = test_utils.create_dummyfridge("Fridge A")
        test_utils.connect_fridge_user(self.user.username, self.fridge.name)
        test_utils.connect_fridge_user(self.user_b.username, self.fridge.name)
        test_utils.create_message_token(tok="fridgify_1", username=self.user.username)
        test_utils.create_message_token(
            tok="hopper_1", username=self.user.username, provider="Hopper"
        )
        test_utils.create_message_token(tok="fridgify_2", username=self.user_b.username)

    def test_get_recipients_exp_recipents_dictionary(self):
        """Get recipients. Expecting dictionary of tokens"""
        recipients = message_handler.get_recipients(self.fridge.fridge_id)

        self.assertTrue(4 in recipients.keys())
        self.assertTrue("fridgify_1", "fridgify_2" in recipients[4])  # pylint: disable=redundant-unittest-assert
        self.assertTrue(5 in recipients.keys())
        self.assertTrue("hopper_1" in recipients[5])
