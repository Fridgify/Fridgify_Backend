from django.test import TestCase
from Fridgify_Backend import view
import json


class ManagementTestCasesDeleteFridge(TestCase):

    """Hello World test case"""
    def test_hello_world(self):
        response = json.loads(view.hello_world("dummy").content)
        self.assertEqual(response["message"], "Hello World", "Hello world")
