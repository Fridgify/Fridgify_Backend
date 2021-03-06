"""Test file for QR Code"""
# pylint: disable=no-member

import json
from unittest.mock import patch

from django.test import TestCase, RequestFactory
from django.utils import timezone

from fridgify_backend.models import Accesstokens, Providers
from fridgify_backend.tests import test_utils
from fridgify_backend.views.fridge.management import qr_code


class QRCodeTestCase(TestCase):
    """TestCase for qr code view"""
    def setUp(self) -> None:
        """Setup for test case"""
        self.factory = RequestFactory()
        test_utils.setup()
        self.user = test_utils.create_dummyuser()
        self.fridge = test_utils.create_dummyfridge()
        test_utils.connect_fridge_user()
        test_utils.create_login_token(
            timezone.now() + timezone.timedelta(days=1),
            username=self.user.username
        )
        test_utils.create_api_token(
            timezone.now() + timezone.timedelta(days=1),
            tok="API Token",
            username=self.user.username
        )
        self.s_request = self.factory.get(f"/fridge/management/{self.fridge.fridge_id}/qr-code")
        self.s_request.META["HTTP_AUTHORIZATION"] = "API Token"

    @patch("fridgify_backend.utils.dynamic_link.create_dynamic_link")
    def test_gen_code_created_token_and_link_exp_201_created(self, dynamic_link):
        """Generate code successfully. Expecting 201 response"""
        exp_link = "https://fridgify.page.link/shortLink"
        dynamic_link.return_value = exp_link

        response = qr_code.gen_code_view(self.s_request, self.fridge.fridge_id)
        self.assertEqual(response.status_code, 201)

        body = json.loads(response.render().content.decode("utf-8"))
        self.assertTrue("dynamic_link" in body)
        self.assertTrue("validation_time" in body)
        self.assertEqual(body["dynamic_link"], exp_link)
        self.assertEqual(body["validation_time"], 43200)

        token_obj = Accesstokens.objects.filter(
            user_id=self.user.user_id,
            fridge_id=self.fridge.fridge_id,
            provider__name="Fridgify-Join"
        ).get()
        self.assertIsNotNone(token_obj)
        self.assertTrue(isinstance(token_obj.accesstoken, str))
        self.assertGreaterEqual(token_obj.valid_till, timezone.now())
        self.assertEqual(token_obj.redirect_url, exp_link)

    def test_gen_code_incorrect_fridge_exp_404_not_found(self):
        """Generate code for non-existent fridge. Expecting 404 response"""
        request = self.factory.get("/fridge/management/999/qr-code")
        request.META["HTTP_AUTHORIZATION"] = "API Token"

        response = qr_code.gen_code_view(request, 999)
        self.assertEqual(response.status_code, 404)

    def test_gen_code_missing_provider_exp_500_internal_error(self):
        """Generate code. Missing provider. Expecting 500 response"""
        Providers.objects.filter(name="Fridgify-Join").delete()

        response = qr_code.gen_code_view(self.s_request, self.fridge.fridge_id)
        self.assertEqual(response.status_code, 500)

        Providers.objects.create(name="Fridgify-Join")

    @patch(
        "fridgify_backend.utils.dynamic_link.create_dynamic_link",
        side_effect=json.JSONDecodeError(msg="Invalid Payload", doc="", pos=0)
    )
    def test_gen_code_bad_request_firebase_exp_500_internal_error(self, mock_dynamic_link):
        """Generate code. Firebase Error. Expecting 500 response"""
        # pylint: disable=unused-argument
        response = qr_code.gen_code_view(self.s_request, self.fridge.fridge_id)
        self.assertEqual(response.status_code, 500)

    def test_gen_code_incorrect_token_exp_403_forbidden(self):
        """Generate code with incorrect token. Expecting 403 response"""
        request = self.factory.get(f"/fridge/management/{self.fridge.fridge_id}/qr-code")
        request.META["HTTP_AUTHORIZATION"] = "API"

        response = qr_code.gen_code_view(request, self.fridge.fridge_id)
        self.assertEqual(response.status_code, 403)
