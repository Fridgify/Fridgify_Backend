"""Test file for Message Content"""

from django.utils import timezone
from django.test import TestCase

from fridgify_backend.utils.messaging import message_content
from fridgify_backend.tests import test_utils


class TestCaseMessageContent(TestCase):
    """TestCase for message content creation"""
    fixtures = [
        "fridgify_backend/fixtures/providers.json",
        "fridgify_backend/tests/fixtures/stores.json"
    ]

    def setUp(self) -> None:
        """Setup for test case"""
        self.user = test_utils.create_dummyuser()
        self.fridge = test_utils.create_dummyfridge("Fridge A")
        self.fridge_b = test_utils.create_dummyfridge("Fridge B")
        test_utils.connect_fridge_user(self.user.username, self.fridge.name)
        test_utils.connect_fridge_user(self.user.username, self.fridge_b.name)
        self.item_a = test_utils.create_items("Item A")
        self.item_b = test_utils.create_items("Item B")
        date = timezone.datetime.now() + timezone.timedelta(days=1)
        date_future = timezone.datetime.now() + timezone.timedelta(days=10)
        test_utils.create_fridge_content(
            self.item_a.item_id,
            self.fridge.fridge_id,
            year=date_future.year,
            month=date_future.month,
            day=date_future.day
        )
        test_utils.create_fridge_content(
            self.item_b.item_id,
            self.fridge.fridge_id,
            year=date.year,
            month=date.month,
            day=date.day
        )
        test_utils.create_fridge_content(
            self.item_a.item_id,
            self.fridge_b.fridge_id,
            year=date.year,
            month=date.month,
            day=date.day
        )

    def test_grouped_content_exp_tuple_list(self):
        """Group to be expired by items by fridge id"""
        content = message_content.get_grouped_content(3)
        print(content)
        self.assertTrue(len(content) == 2)
        self.assertEqual(content[0][0], self.fridge.fridge_id)
        self.assertEqual(content[0][1][0]["item_id"], self.item_b.item_id)
        self.assertEqual(content[0][1][0]["item__name"], self.item_b.name)
        self.assertEqual(content[0][1][0]["fridge_id"], self.fridge.fridge_id)
        self.assertEqual(content[1][0], self.fridge_b.fridge_id)
        self.assertEqual(content[1][1][0]["item_id"], self.item_a.item_id)
        self.assertEqual(content[1][1][0]["item__name"], self.item_a.name)
        self.assertEqual(content[1][1][0]["fridge_id"], self.fridge_b.fridge_id)

    def test_create_expired_message(self):
        """Create a message which lists expired items"""
        message = message_content.create_expired_message(
            self.fridge.fridge_id,
            [{'item_id': 2, 'item__name': 'Item B', 'fridge_id': 1, 'item_count': 1}],
            3
        )
        exp_message = "Hey there! Your fridge Fridge A contains items, " \
                      "which are going to expire in the next 3 days:\n1x Item B" \
                      "\nCheck them out!"
        self.assertEqual(message["title"], "Fridge A: Items about to expire")
        self.assertEqual(message["body"], exp_message.strip())

    def test_create_expired_message_overflowed(self):
        """Create a message which lists expired items"""
        message = message_content.create_expired_message(
            self.fridge.fridge_id,
            [
                {'item_id': 2, 'item__name': 'Item B', 'fridge_id': 1, 'item_count': 1},
                {'item_id': 3, 'item__name': 'Item C', 'fridge_id': 1, 'item_count': 2},
                {'item_id': 4, 'item__name': 'Item D', 'fridge_id': 1, 'item_count': 3},
                {'item_id': 5, 'item__name': 'Item D', 'fridge_id': 1, 'item_count': 10}
            ],
            3
        )
        exp_message = "Hey there! Your fridge Fridge A contains items, " \
                      "which are going to expire in the next 3 days:\n" \
                      "1x Item B, 2x Item C, 3x Item D" \
                      "\nand 10 other items, which are about to expire as well.\n" \
                      "Check them out!"
        self.assertEqual(message["title"], "Fridge A: Items about to expire")
        self.assertEqual(message["body"], exp_message.strip())

    def test_rest_amount(self):
        """Count rest items"""
        amount = message_content.rest_amount(
            [
                {'item_id': 2, 'item__name': 'Item B', 'fridge_id': 1, 'item_count': 1},
                {'item_id': 5, 'item__name': 'Item B', 'fridge_id': 1, 'item_count': 10}
            ]
        )
        self.assertEqual(amount, 11)
