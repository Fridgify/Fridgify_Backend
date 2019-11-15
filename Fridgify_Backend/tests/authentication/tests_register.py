from django.test import TestCase
from Fridgify_Backend.views.authentication import register
import json


class AuthenticationTestCasesRegister(TestCase):

    """Register test case"""
    def test_register(self):
        response = json.loads(register.entry_point("dummy").content)
        self.assertEqual(response["message"], "register", "Test register")
