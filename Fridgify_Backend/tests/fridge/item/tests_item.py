from django.test import TestCase
from Fridgify_Backend.views.fridge.item import item
import json


class ItemTestCasesItem(TestCase):

    """Get item test case"""
    def test_hello_world(self):
        response = json.loads(item.entry_point("dummy").content)
        self.assertEqual(response["message"], "Get item", "Get item")
