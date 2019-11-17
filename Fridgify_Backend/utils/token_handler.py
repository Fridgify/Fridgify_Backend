import secrets
import datetime
from django.utils import timezone
import json

from Fridgify_Backend.models.accesstokens import Accesstokens
from Fridgify_Backend.models.providers import Providers
from Fridgify_Backend.models.users import Users


def generate_token(request, internal_provider):
    """ Generate a token for our internal providers

    :param request: Request containing username, password
    :param internal_provider: Either Fridgify or Fridgify-API
    :return: Generic Token
    """
    print("Generating token for internal provider...")
    reqj = json.load(request)
    # Retrieve existing tokens, wipe outdated tokens
    token = existing_tokens(reqj["username"], internal_provider)

    # If no token existing, create a new one
    if token is None:
        token = secrets.token_hex(32)
        db_token = Accesstokens()
        db_token.accesstoken = token
        db_token.provider = Providers.objects.filter(name=internal_provider).first()
        db_token.valid_till = timezone.now() + timezone.timedelta(days=14)
        db_token.user = Users.objects.filter(username=reqj["username"]).first()
        db_token.save()

    return token


def existing_tokens(username, internal_provider):
    """ Check if a token already exists

    :param username: name of user
    :param internal_provider: Either Fridgify or Fridgify-API
    :return: existing token or none
    """
    print("Check if token already exists...")
    token_objs = Accesstokens.objects.filter(user__username=username, provider__name=internal_provider)
    if len(token_objs) > 0:
        if is_token_valid(token_objs):
            return token_objs.values("accesstoken").first()
        else:
            return None


def is_token_valid(token_objs):
    """ Check if a token is still valid

    :param token_objs: Entries matching user and provider
    :return: valid - True | invalid - False
    """
    print("Check validity of token...")
    valid_till = token_objs.values_list("valid_till").first()
    print(valid_till[0])
    if timezone.now() > valid_till[0]:
        token_objs.first().delete()
        return False
    else:
        return True
