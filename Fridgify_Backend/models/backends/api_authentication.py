from django.utils import timezone

from rest_framework import authentication
from rest_framework import exceptions

from Fridgify_Backend.models import Accesstokens


class APIAuthentication(authentication.BaseAuthentication):
    """
    Backend is responsible for API authentication via a valid API-Token.
    A request header is required to have an "Authorization"-Header, which contains the valid API-Token.
    """
    def authenticate(self, request):
        if "Authorization" in request.headers:
            req_token = request.headers["Authorization"]
            try:
                token = Accesstokens.objects.get(
                    accesstoken=req_token,
                    provider__name="Fridgify-API",
                    valid_till__gte=timezone.now(),
                )
                token.user.is_authenticated = True
                token.user.token_authentication = token.accesstoken
                return token.user, None
            except Accesstokens.DoesNotExist or Accesstokens.MultipleObjectsReturned:
                raise exceptions.AuthenticationFailed
        raise exceptions.AuthenticationFailed
