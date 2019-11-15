from django.test import TestCase
from Fridgify_Backend.views.fridge.content import fridge_content_item
import json


class ContentApiTestCasesFridgeContentItem(TestCase):

    """Add fridge content item test case"""
    def test_add_fridge_content_item(self):
        response = json.loads(fridge_content_item.entry_point("POST").content)
        self.assertEqual(response["message"], "Add item", "Add item")

    """Get fridge content item test case"""
    def test_get_fridge_content_item(self):
        response = json.loads(fridge_content_item.entry_point("GET").content)
        self.assertEqual(response["message"], "Get item", "Get item")

    """Delete fridge content item test case"""
    def test_delete_fridge_content_item(self):
        response = json.loads(fridge_content_item.entry_point("DELETE").content)
        self.assertEqual(response["message"], "Delete item", "Delete item")
