from django.test import TestCase
from Fridgify_Backend.views.fridge.management import create_fridge
import json


class ManagementTestCasesCreateFridge(TestCase):

    """Create fridge test case"""
    def test_create_fridge(self):
        response = json.loads(create_fridge.entry_point("dummy").content)
        self.assertEqual(response["message"], "create fridge", "create fridge")
