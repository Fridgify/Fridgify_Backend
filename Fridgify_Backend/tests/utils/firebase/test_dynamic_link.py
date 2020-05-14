import json
from unittest.mock import patch

from django.test import TestCase

from Fridgify_Backend.utils.firebase import dynamic_link


class DynamicLinkTestCase(TestCase):
    @patch("Fridgify_Backend.utils.firebase.dynamic_link.requests.post")
    def test_successfulRequest_ShortLink(self, mock_post):
        exp_link = "https://fridgify.page.link/shortStuff"
        mock_post.return_value.content = json.dumps({"shortLink": exp_link})
        mock_post.return_value.status_code = 200

        link = dynamic_link.create_dynamic_link("Token123", "Prefix")
        self.assertEqual(link, exp_link)

    @patch("Fridgify_Backend.utils.firebase.dynamic_link.requests.post")
    def test_malformedBody_APIException(self, mock_post):
        mock_post.return_value.content = ""
        mock_post.return_value.status_code = 400

        self.assertRaises(json.decoder.JSONDecodeError, dynamic_link.create_dynamic_link, "TokenBla", "Prefix")
