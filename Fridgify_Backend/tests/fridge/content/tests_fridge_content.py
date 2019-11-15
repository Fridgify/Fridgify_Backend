from django.test import TestCase
from Fridgify_Backend.views.fridge.content import fridge_content
import json


class ContentApiTestCasesFridgeContent(TestCase):

    """Add fridge content test case"""
    def test_add_fridge_content(self):
        response = json.loads(fridge_content.entry_point("POST").content)
        self.assertEqual(response["message"], "Add content", "Add content")

    """Get fridge content test case"""
    def test_get_fridge_content(self):
        response = json.loads(fridge_content.entry_point("GET").content)
        self.assertEqual(response["message"], "Get content", "Get content")
