import datetime
from django.test import TestCase, RequestFactory
from unittest import mock

from Fridgify_Backend.utils import login_handler
from Fridgify_Backend.models.users import Users
from Fridgify_Backend.models.providers import Providers


class UtilsTestCasesLoginHandler(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        Users.objects.create(username="dummy_name", name="Dummy", surname="Name", email="dummy@dumdum.dum",
                             password="$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS",
                             birth_date=datetime.date(2000, 1, 1))
        Providers.objects.create(name="Fridgify")
        Providers.objects.create(name="Fridgify-API")

    @mock.patch('Fridgify_Backend.utils.login_handler.retrieve_password')
    def test_checkCredentials_ValidCredentials_1(self, mock_retrieve_password):
        mock_retrieve_password.return_value = "$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS"
        request = self.factory.post("/auth/login/", {"username": "dummy_name", "password": "password"},
                                    content_type="application/json")
        auth = login_handler.check_credentials(request)
        self.assertEqual(1, auth)

    @mock.patch('Fridgify_Backend.utils.login_handler.retrieve_password')
    def test_checkCredentials_InvalidCredentials_1(self, mock_retrieve_password):
        mock_retrieve_password.return_value = "$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS"
        request = self.factory.post("/auth/login/", {"username": "dummy_name", "password": "notapassword"},
                                    content_type="application/json")
        auth = login_handler.check_credentials(request)
        self.assertEqual(0, auth)

    def test_checkCredentials_MissingUsername_minus1(self):
        request = self.factory.post("/auth/login/", {"password": "password"},
                                    content_type="application/json")
        auth = login_handler.check_credentials(request)
        self.assertEqual(-1, auth)

    @mock.patch('Fridgify_Backend.utils.login_handler.retrieve_password')
    def test_checkCredentials_NothingFound_0(self, mock_retrieve_password):
        mock_retrieve_password.return_value = "$2b$12$1hKYhKg4lo9Bd4jES8qjRYOjInaIObjn0JJ8SlWPOpR9MzKcseMDVS"
        request = self.factory.post("/auth/login/", {"username": "imnotexistingslol", "password": "password"},
                                    content_type="application/json")
        auth = login_handler.check_credentials(request)
        self.assertEqual(0, auth)
