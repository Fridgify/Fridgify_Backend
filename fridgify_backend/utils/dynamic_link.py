"""Handle dynamic links"""

import json
import logging
import os
import requests


logger = logging.getLogger(__name__)


def create_dynamic_link(deep_link):
    """Create a Firebase dynamic link for the passed deep link"""
    logger.info("Creating dynamic link via Firebase...")
    logger.debug("Deep Link: %s", deep_link)

    payload = {
        "dynamicLinkInfo": {
            "domainUriPrefix": os.environ['FRIDGIFY_DL_URL'],
            "link": deep_link,
            "androidInfo": {"androidPackageName": os.environ['ANDROID_PN']},
            "iosInfo": {"iosBundleId": os.environ['IOS_BID']}
        }
    }
    logger.debug("Payload: %s", repr(payload))

    req_url = f"{os.environ['FB_DL_URL']}/shortLinks?key={os.environ['FB_API_KEY']}"
    response = requests.post(req_url, data=json.dumps(payload))
    logger.debug("Firebase Response: %s", response.content)
    if response.status_code != 200:
        raise json.JSONDecodeError(msg="Invalid Payload", doc="", pos=0)
    content = json.loads(response.content)
    return content["shortLink"]


def create_deep_link(prefix, **kwargs):
    """Create a deep link"""
    path = []
    for key, value in kwargs.items():
        path.append(f"{key}={value}")
    deep_link = f"{os.environ['BASE_URL']}{prefix}?{'&'.join(path)}"
    return deep_link
