from django.test import TestCase
from Fridgify_Backend.views.fridge.management import join_fridge
import json


class ManagementTestCasesJoinFridge(TestCase):

    """Join fridge test case"""
    def test_join_fridge(self):
        response = json.loads(join_fridge.entry_point("dummy").content)
        self.assertEqual(response["message"], "Join fridge", "Join fridge")
