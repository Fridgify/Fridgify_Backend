import json
import datetime
from django.utils import timezone
from django.test import TestCase, RequestFactory
from unittest import mock

from Fridgify_Backend.utils import register_handler
from Fridgify_Backend.models.users import Users
from Fridgify_Backend.models.providers import Providers


class UtilsTestCasesRegisterHandler(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        Users.objects.create(username="dummy_name", name="Dummy", surname="Name", email="dummy@dumdum.dum",
                             password="$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS",
                             birth_date=datetime.date(2000, 1, 1))
        Providers.objects.create(name="Fridgify")
        Providers.objects.create(name="Fridgify-API")

    @mock.patch("Fridgify_Backend.utils.register_handler.check_body")
    def test_register_ValidRequest_Created(self, mock_check):
        mock_check.return_value = True
        request = self.factory.post("/auth/register", {"username": "newbie", "password": "password2",
                                                       "email": "newbie@nub.de", "name": "Newbie", "surname": "Noob",
                                                       "birthdate": "2000-12-17"}, content_type="application/json")
        response = register_handler.register(request)
        self.assertEqual(response, 1)
        obj = Users.objects.filter(username="newbie").values()
        self.assertEqual(len(obj), 1)
        self.assertEqual(obj.first()["username"], "newbie")

    @mock.patch("Fridgify_Backend.utils.register_handler.check_body")
    def test_register_UsernameExists_Created(self, mock_check):
        mock_check.return_value = True
        request = self.factory.post("/auth/register", {"username": "dummy_name", "password": "password2",
                                                       "email": "newbie@nub.de", "name": "Newbie", "surname": "Noob",
                                                       "birthdate": "2000-12-17"}, content_type="application/json")
        response = register_handler.register(request)
        self.assertEqual(response, -2)
        obj = Users.objects.all()
        self.assertEqual(len(obj), 1)

    @mock.patch("Fridgify_Backend.utils.register_handler.check_body")
    def test_register_EmailExists_Created(self, mock_check):
        mock_check.return_value = True
        request = self.factory.post("/auth/register", {"username": "newbie", "password": "password2",
                                                       "email": "dummy@dumdum.dum", "name": "Newbie", "surname": "Noob",
                                                       "birthdate": "2000-12-17"}, content_type="application/json")
        response = register_handler.register(request)
        self.assertEqual(response, -3)
        obj = Users.objects.all()
        self.assertEqual(len(obj), 1)

    @mock.patch("Fridgify_Backend.utils.register_handler.check_body")
    def test_register_InvalidRequest_NotCreated(self, mock_check):
        mock_check.return_value = False
        request = self.factory.post("/auth/register", {"username": "newbie", "password": "password2",
                                                       "email": "dummy@dumdum.dum", "name": "Newbie", "surname": "Noob",
                                                       "birthdate": "2000-12-17"}, content_type="application/json")
        response = register_handler.register(request)
        self.assertEqual(response, 0)
        obj = Users.objects.all()
        self.assertEqual(len(obj), 1)

    def test_checkBody_Valid_True(self):
        req_body = json.dumps({"username": "newbie", "password": "password2",
                               "email": "dummy@dumdum.dum", "name": "Newbie", "surname": "Noob",
                               "birthdate": "2000-12-17"})
        res = register_handler.check_body(req_body)
        self.assertEqual(res, True)
