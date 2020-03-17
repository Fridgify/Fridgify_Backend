from django.test import TestCase
from Fridgify_Backend.views.fridge.management import edit_fridge
import json


class ManagementTestCasesGeneral(TestCase):

    """Management test case"""
    def test_hello_world(self):
        response = json.loads(edit_fridge.entry_point("dummy").content)
        self.assertEqual(response["message"], "Management", "Management")
