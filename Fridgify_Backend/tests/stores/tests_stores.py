from django.test import TestCase
from Fridgify_Backend.views.stores import stores
import json


class StoresTestCases(TestCase):

    """Add store test case"""
    def test_add_store(self):
        response = json.loads(stores.entry_point("POST").content)
        self.assertEqual(response["message"], "Add store", "Add store")

    """Get store test case"""
    def test_get_store(self):
        response = json.loads(stores.entry_point("GET").content)
        self.assertEqual(response["message"], "Get store", "Get store")
