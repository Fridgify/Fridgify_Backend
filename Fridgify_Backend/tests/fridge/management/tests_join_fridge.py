from django.test import TestCase, RequestFactory
from django.utils import timezone

from Fridgify_Backend.models import UserFridge, Accesstokens
from Fridgify_Backend.views.fridge.management import join_fridge
from Fridgify_Backend.tests import test_utils


class ManagementTestCasesJoinFridge(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        test_utils.setup()
        self.user = test_utils.create_dummyuser()
        self.user2 = test_utils.create_dummyuser(username="User2", email="user2@mail.de")
        self.fridge = test_utils.create_dummyfridge()
        test_utils.connect_fridge_user()
        test_utils.create_login_token(timezone.now() + timezone.timedelta(days=1), username=self.user.username)
        test_utils.create_api_token(
            timezone.now() + timezone.timedelta(days=1), t="API Token", username=self.user2.username
        )
        test_utils.create_api_token(
            timezone.now() + timezone.timedelta(days=1), t="Already in Fridge", username=self.user.username
        )

        self.token = "jointoken"
        test_utils.create_join_token(t=self.token, fridge=self.fridge)
        self.s_request = self.factory.get(f"/fridge/management/join?token={self.token}")
        self.s_request.META["HTTP_AUTHORIZATION"] = "API Token"

    def test_validJoinToken_201Created(self):
        response = join_fridge.join_view(self.s_request)
        self.assertEqual(response.status_code, 201)

        uf = UserFridge.objects.filter(user_id=self.user.user_id, fridge_id=self.fridge.fridge_id)
        self.assertTrue(uf.exists())

    def test_noJoinToken_400BadRequest(self):
        request = self.factory.get(f"/fridge/management/join")
        request.META["HTTP_AUTHORIZATION"] = "API Token"
        response = join_fridge.join_view(request)
        self.assertEqual(response.status_code, 400)

    def test_joinTokenNotExistent_404NotFound(self):
        request = self.factory.get(f"/fridge/management/join?token=ThisShouldAbsolutelyNotWork")
        request.META["HTTP_AUTHORIZATION"] = "API Token"
        response = join_fridge.join_view(request)
        self.assertEqual(response.status_code, 404)

    def test_joinTokenNotExistent_409Conflict(self):
        request = self.factory.get(f"/fridge/management/join?token={self.token}")
        request.META["HTTP_AUTHORIZATION"] = "Already in Fridge"
        response = join_fridge.join_view(request)
        self.assertEqual(response.status_code, 409)

    def test_linkNotValid_410Gone(self):
        token = Accesstokens.objects.get(
            provider__name="Fridgify-Join", accesstoken=self.token, fridge=self.fridge, user=self.user
        )
        token.valid_till = timezone.now() - timezone.timedelta(days=15)
        token.save()

        response = join_fridge.join_view(self.s_request)
        self.assertEqual(response.status_code, 410)
        self.assertFalse(Accesstokens.objects.filter(
            provider__name="Fridgify-Join", accesstoken=self.token, fridge=self.fridge, user=self.user
        ).exists())

        test_utils.create_join_token(t=self.token, fridge=self.fridge)
