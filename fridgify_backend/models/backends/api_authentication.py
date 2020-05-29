"""
Backend which handles authentication for API
"""

import logging

from django.utils import timezone
from rest_framework import authentication
from rest_framework import exceptions

from fridgify_backend.models import Accesstokens


logger = logging.getLogger(__name__)


class APIAuthentication(authentication.BaseAuthentication):
    """
    Backend is responsible for API authentication via a valid API-Token.
    A request header is required to have an "Authorization"-Header,
    which contains the valid API-Token.
    """
    def authenticate(self, request):
        if "Authorization" in request.headers:
            req_token = request.headers["Authorization"]
            logger.info('Authenticate via %s...', repr(req_token))
            try:
                token = Accesstokens.objects.get(  # pylint: disable=no-member
                    accesstoken=req_token,
                    provider__name="Fridgify-API",
                    valid_till__gte=timezone.now(),
                )
                token.user.is_authenticated = True
                token.user.token_authentication = token.accesstoken
                logger.debug("User for token (%s) = %s", repr(req_token), token.user.username)
                return token.user, None
            except Accesstokens.DoesNotExist:  # pylint: disable=no-member
                logger.error("Login-Token %s does not exist...", repr(req_token))
                raise exceptions.AuthenticationFailed
            except Accesstokens.MultipleObjectsReturned:  # pylint: disable=no-member
                logger.error("%s - Multiple tokens exist."
                             "This should not happen...", repr(req_token))
                raise exceptions.APIException(detail="Internal Server Error (Token Error)")
        logger.error("No Login-Token provided...")
        raise exceptions.AuthenticationFailed
