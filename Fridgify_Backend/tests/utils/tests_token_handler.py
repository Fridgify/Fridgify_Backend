import datetime
from django.test import TestCase, RequestFactory
from unittest import mock

from Fridgify_Backend.models.users import Users
from Fridgify_Backend.models.providers import Providers
from Fridgify_Backend.utils import token_handler


class UtilsTestCasesTokenHandler(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        Users.objects.create(username="dummy_name", name="Dummy", surname="Name", email="dummy@dumdum.dum",
                             password="$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS",
                             birth_date=datetime.date(2000, 1, 1))
        Providers.objects.create(name="Fridgify")
        Providers.objects.create(name="Fridgify-API")

    @mock.patch('Fridgify_Backend.utils.token_handler.existing_tokens')
    def test_generateToken_NoExistingTokenAndProviderFridgify_newToken(self, mock_existing_tokens):
        mock_existing_tokens.return_value = None
        token_handler.generate_token("dummy_name", "Fridgify")
        #TODO:
        print()

