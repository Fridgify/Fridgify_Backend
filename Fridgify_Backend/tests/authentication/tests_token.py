from django.test import TestCase
from Fridgify_Backend.views.authentication import token
import json


class AuthenticationTestCasesToken(TestCase):

    """Token test case"""
    def test_token(self):
        response = json.loads(token.entry_point("dummy").content)
        self.assertEqual(response["message"], "token", "Test token")
