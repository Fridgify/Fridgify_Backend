from django.test import TestCase, RequestFactory
from rest_framework import status
from Fridgify_Backend.models.users import Users
from Fridgify_Backend.models.providers import Providers
from Fridgify_Backend.models.fridges import Fridges
from Fridgify_Backend.models.user_fridge import UserFridge
from Fridgify_Backend.views.fridge.management import create_fridge
from Fridgify_Backend.views.authentication import login, token
from Fridgify_Backend.utils.test_utils import create_providers

import json
import datetime


class ManagementTestCasesCreateFridge(TestCase):


    def setUp(self):
        self.factory = RequestFactory()
        user = Users.objects.create(username="dummy_name", name="Dummy", surname="Name", email="dummy@dumdum.dum",
                             password="$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS",
                             birth_date=datetime.date(2000, 1, 1))
        create_providers()
        fridge = Fridges.objects.create(name="Miau", description="adsdsadad")
        request_login = self.factory.post("/auth/login/", {"username": "dummy_name", "password": "password"},
                                    content_type="application/json")
        api_token = json.loads(login.login(request_login).content)["token"]
        request_token = self.factory.get("/auth/token/")
        header = {"Authorization": api_token}
        request_token.__setattr__("headers", header)
        self.token = json.loads(token.get_response(request_token).content)["token"]
        UserFridge.objects.create(fridge_id=fridge.fridge_id, user_id=user.user_id)

    """Create fridge test case"""
    def test_create_fridge_body_validation(self):
        request_no_body = self.factory.post("/fridge/management/create/", content_type="application/json")
        header = {"Authorization": self.token}
        request_no_body.__setattr__("headers", header)
        response_no_body = create_fridge.entry_point(request_no_body)
        self.assertEqual(response_no_body.status_code, status.HTTP_400_BAD_REQUEST, "Body is not present")
        self.assertEqual(json.loads(response_no_body.content)["message"], "Missing parameters. Required are name and description"
                         , "Body is not present")

        request_wrong_keys = self.factory.post("/fridge/management/create/", {
            "Cat": "Miau",
            "askdakdmlkad": "adsdsadad"
        }, content_type="application/json")
        request_wrong_keys.__setattr__("headers", header)
        response_wrong_keys = create_fridge.entry_point(request_wrong_keys)
        self.assertEqual(response_wrong_keys.status_code, status.HTTP_400_BAD_REQUEST, "Body is not present")
        self.assertEqual(json.loads(response_wrong_keys.content)["message"], "Missing parameters. Required are name and description"
                         , "Body is not present")

        request_duplicate_entry = self.factory.post("/fridge/management/create/", {
            "name": "Miau",
            "description": "adsdsadad"
        }, content_type="application/json")
        request_duplicate_entry.__setattr__("headers", header)
        response_duplicate_entry = create_fridge.entry_point(request_duplicate_entry)
        self.assertEqual(response_duplicate_entry.status_code, status.HTTP_409_CONFLICT, "Duplicate fridge")
        self.assertEqual(json.loads(response_duplicate_entry.content)["message"], "Fridge Miau already exists for user", "Duplicate fridge")

        request_correct = self.factory.post("/fridge/management/create/", {
            "name": "Wuff",
            "description": "adsdsadad"
        }, content_type="application/json")
        request_correct.__setattr__("headers", header)
        response_correct = create_fridge.entry_point(request_correct)
        self.assertEqual(response_correct.status_code, status.HTTP_201_CREATED, "Created fridge")
        self.assertEqual(json.loads(response_correct.content)["message"], "Created", "Created fridge")
