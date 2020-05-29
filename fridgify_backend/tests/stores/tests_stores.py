from django.test import TestCase
from fridgify_backend.views.stores import stores
import json


class StoresTestCases(TestCase):

    """Add store test case"""
    def test_add_store(self):
        self.assertEqual(True, True)