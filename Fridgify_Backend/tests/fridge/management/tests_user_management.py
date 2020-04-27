from django.test import TestCase, RequestFactory
from django.utils import timezone

from rest_framework import status
from Fridgify_Backend.models import UserFridge
from Fridgify_Backend.views.fridge.management import users
from Fridgify_Backend.tests import test_utils

import json


class TestUserManagement(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        test_utils.setup()
        self.user = []
        self.user.append(test_utils.create_dummyuser(username="Test User", name="Test", surname="User", email="test@user.de"))
        self.user.append(test_utils.create_dummyuser(username="Test User 2", name="Test 2", surname="User 2", email="test@user2.de"))
        self.user.append(test_utils.create_dummyuser(username="Test User 3", name="Test 3", surname="User 3", email="test@user3.de"))
        self.fridge = test_utils.create_dummyfridge(name="Test Fridge")

        test_utils.connect_fridge_user(username=self.user[0].username, fridge=self.fridge.name, role=UserFridge.OWNER)
        test_utils.connect_fridge_user(username=self.user[1].username, fridge=self.fridge.name, role=UserFridge.OVERSEER)
        test_utils.connect_fridge_user(username=self.user[2].username, fridge=self.fridge.name, role=UserFridge.USER)

        test_utils.create_login_token(timezone.now() + timezone.timedelta(days=1), username=self.user[0].username)
        test_utils.create_api_token(timezone.now() + timezone.timedelta(days=1), t="API Token User1", username=self.user[0].username)

        test_utils.create_login_token(timezone.now() + timezone.timedelta(days=1), username=self.user[1].username)
        test_utils.create_api_token(timezone.now() + timezone.timedelta(days=1), t="API Token User2", username=self.user[1].username)

        test_utils.create_login_token(timezone.now() + timezone.timedelta(days=1), username=self.user[2].username)
        test_utils.create_api_token(timezone.now() + timezone.timedelta(days=1), t="API Token User3", username=self.user[2].username)
        return super().setUp()

    def test_listUsers_success(self):
        request = self.factory.get(f"/fridge/management/{self.fridge.fridge_id}/users")
        request.META["HTTP_AUTHORIZATION"] = "API Token User1"

        response = users.fridge_users_view(request, self.fridge.fridge_id)

        content = json.loads(response.render().content)

        exp_resp = [
            {
                "user": {
                    "username": "Test User", "name": "Test", "surname": "User", "email": "test@user.de", "birth_date": "2000-10-17"
                },
                "role": "Fridge Owner"
            }, {
                "user": {
                    "username": "Test User 2", "name": "Test 2", "surname": "User 2", "email": "test@user2.de", "birth_date": "2000-10-17"
                },
                "role": "Fridge Overseer"
            }, {
                "user": {
                    "username": "Test User 3", "name": "Test 3", "surname": "User 3", "email": "test@user3.de", "birth_date": "2000-10-17"
                },
                "role": "Fridge User"
            }
        ]
        self.assertEqual(exp_resp, content)
        self.assertEqual(response.status_code, 200)

    def test_editRole_asOwner_targetOverseer_toUser_Changed200(self):
        request = self.factory.patch(
            f"/fridge/management/{self.fridge.fridge_id}/users/{self.user[1].user_id}",content_type="application/json",
            data={
                "role": "Fridge User"
            })
        request.META["HTTP_AUTHORIZATION"] = "API Token User1"

        response = users.user_role_view(request, self.fridge.fridge_id, self.user[1].user_id)

        content = json.loads(response.render().content)

        self.assertEqual(response.status_code, 200)

        exp_resp =  {
            "user": {
                "username": "Test User 2", "name": "Test 2", "surname": "User 2", "email": "test@user2.de", "birth_date": "2000-10-17"
            },
            "role": "Fridge User"
        }
        self.assertEqual(content, exp_resp)    
        self.assertEqual(2, UserFridge.objects.filter(user_id=self.user[1].user_id).get().role)


        uf = UserFridge.objects.filter(user_id=self.user[1].user_id).get()
        uf.role = 1

    def test_editRole_asOverseer_targetUser_toOverseer_Changed200(self):
        request = self.factory.patch(
            f"/fridge/management/{self.fridge.fridge_id}/users/{self.user[2].user_id}",content_type="application/json",
            data={
                "role": "Fridge Overseer"
            })
        request.META["HTTP_AUTHORIZATION"] = "API Token User2"

        response = users.user_role_view(request, self.fridge.fridge_id, self.user[2].user_id)

        content = json.loads(response.render().content)

        self.assertEqual(response.status_code, 200)

        exp_resp =  {
            "user": {
                "username": "Test User 3", "name": "Test 3", "surname": "User 3", "email": "test@user3.de", "birth_date": "2000-10-17"
            },
            "role": "Fridge Overseer"
        }
        self.assertEqual(content, exp_resp)    
        self.assertEqual(1, UserFridge.objects.filter(user_id=self.user[2].user_id).get().role)


        uf = UserFridge.objects.filter(user_id=self.user[2].user_id).get()
        uf.role = 2

    def test_editRole_asOverseer_targetOwner_Forbidden403(self):
        request = self.factory.patch(
            f"/fridge/management/{self.fridge.fridge_id}/users/{self.user[0].user_id}",content_type="application/json",
            data={
                "role": "Fridge Overseer"
            })
        request.META["HTTP_AUTHORIZATION"] = "API Token User2"

        response = users.user_role_view(request, self.fridge.fridge_id, self.user[0].user_id)

        content = json.loads(response.render().content)

        self.assertEqual(response.status_code, 403)

    def test_editRole_asOverseer_targetSelf_failed(self):
        request = self.factory.patch(
            f"/fridge/management/{self.fridge.fridge_id}/users/{self.user[1].user_id}",content_type="application/json",
            data={
                "role": "Fridge User"
            })
        request.META["HTTP_AUTHORIZATION"] = "API Token User2"

        response = users.user_role_view(request, self.fridge.fridge_id, self.user[1].user_id)

        content = json.loads(response.render().content)

        self.assertEqual(response.status_code, 409)

    def test_editRole_asOverseer_targetSelf_RoleNotExisting406(self):
        request = self.factory.patch(
            f"/fridge/management/{self.fridge.fridge_id}/users/{self.user[1].user_id}",content_type="application/json",
            data={
                "role": "Fridge This Does Not Exist"
            })
        request.META["HTTP_AUTHORIZATION"] = "API Token User1"

        response = users.user_role_view(request, self.fridge.fridge_id, self.user[1].user_id)

        content = json.loads(response.render().content)

        self.assertEqual(response.status_code, 406)
