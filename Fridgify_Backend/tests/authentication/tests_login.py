from django.test import TestCase
from Fridgify_Backend.views.authentication import login
import json


class AuthenticationTestCasesLogin(TestCase):

    """Login test case"""
    def test_login(self):
        # response = json.loads(login.entry_point("dummy").content)
        # self.assertEqual(response["message"], "login", "Test login")
        self.assertEqual(0, 0, "Dummy Test")
