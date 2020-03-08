import time

from rest_framework import authentication
from rest_framework import exceptions

from Fridgify_Backend.models import Accesstokens


class APIAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.headers["Authorization"]
        try:
            token = Accesstokens.objects.get(
                accesstoken=token,
                provider="Fridgify-API",
                valid_till__gte=time.time()
            )
        except Accesstokens.DoesNotExist or Accesstokens.MultipleObjectsReturned:
            return exceptions.AuthenticationFailed

        return token.user, None
