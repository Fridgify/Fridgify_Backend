from django.test import TestCase, RequestFactory
from rest_framework import status
from Fridgify_Backend.models.users import Users
from Fridgify_Backend.models.fridges import Fridges
from Fridgify_Backend.models.user_fridge import UserFridge
from Fridgify_Backend.utils.init_dummy_user import fill_fridges
from Fridgify_Backend.views.fridge.management import create_fridge
from Fridgify_Backend.views.authentication import login
from Fridgify_Backend.utils.test_utils import create_providers

import json
import datetime


class ManagementTestCasesCreateFridge(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = Users.objects.create(username="dummy_name", name="Dummy", surname="Name", email="dummy@dumdum.dum",
                                    password="$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS",
                                    birth_date=datetime.date(2000, 1, 1))
        self.user2 = Users.objects.create(username="testUser", name="Test", surname="User", email="test@user.dum",
                                     password="$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS",
                                     birth_date=datetime.date(2000, 1, 1))
        create_providers()
        fridge = Fridges.objects.create(name="Miau", description="adsdsadad")
        fill_fridges([fridge])
        fridge2 = Fridges.objects.create(name="Wuff", description="adsdsadad")
        UserFridge.objects.create(fridge_id=fridge.fridge_id, user_id=self.user.user_id)
        UserFridge.objects.create(fridge_id=fridge2.fridge_id, user_id=self.user2.user_id)

    def test_user_1_has_1_fridge(self):
        fridges = UserFridge.objects.filter(user_id=self.user.user_id)
        self.assertEqual(len(fridges), 1, "User has more than one fridge")

    def test_user_1_has_the_correct_fridge(self):
        user_fridges = UserFridge.objects.filter(user_id=self.user.user_id)
        for user_fridge in user_fridges:
            fridge = Fridges.objects.get(fridge_id=user_fridge.fridge_id)
            self.assertEqual(fridge.name, "Miau", "User has the wrong fridge")

    def test_user_2_has_1_fridge(self):
        fridges = UserFridge.objects.filter(user_id=self.user.user_id)
        self.assertEqual(len(fridges), 1, "User2 has more than one fridge")

    def test_user_2_has_the_correct_fridge(self):
        user_fridges = UserFridge.objects.filter(user_id=self.user2.user_id)
        for user_fridge in user_fridges:
            fridge = Fridges.objects.get(fridge_id=user_fridge.fridge_id)
            self.assertEqual(fridge.name, "Wuff", "User2 has the wrong fridge")

    def fridge_content_total_is_not_less_than_sum(self):
        fridges = UserFridge.objects.filter(user_id=self.user.user_id)
        for fridge in fridges:
            self.assertGreaterEqual(fridge.content.fresh + fridge.content.overDue + fridge.content.dueSoon,
                                    fridge.content.total, "Fridge content calculation is off. "
                                                          "Total has to be more than or equal the sum off fresh, "
                                                          "overDue and dueSoon")
