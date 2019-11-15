from django.test import TestCase
from Fridgify_Backend import view
from Fridgify_Backend.models.stores import Stores
import json


class ApiTestCases(TestCase):

    """Hello World test case"""
    def test_hello_world(self):
        response = json.loads(view.hello_world("dummy").content)
        self.assertEqual(response["message"], "Hello World", "Hello world")

    def test_insert(self):
        Stores.objects.create(name="Test")
        self.assertGreater(len(Stores.objects.all()), 0, "Test could not be inserted into database")

    def test_read(self):
        Stores.objects.create(name="Test2")
        for e in Stores.objects.all():
            self.assertEqual(e.name, "Test2", "Test2 was not read successfully from database")
