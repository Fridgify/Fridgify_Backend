"""Create message content for messaging services"""
# pylint: disable=no-member

import itertools

from django.db.models import Count, F
from django.utils import timezone

from fridgify_backend import models


def get_grouped_content(due_in):
    """Group to be expired fridge content by fridge_id"""
    content = models.FridgeContent.objects.values(
        "item_id",
        "item__name",
        "fridge_id",
    ).annotate(
        item_count=Count("item_id")
    ).filter(
        expiration_date__range=[
            timezone.datetime.now(),
            timezone.datetime.now() + timezone.timedelta(days=due_in)
        ],
    ).order_by("fridge_id", "item_id")

    return [
        (key, list(value))
        for key, value in itertools.groupby(
            content, key=lambda entry: entry["fridge_id"]
        )
    ]


def create_expired_message(fridge_id, content, due_in, limit=3):
    """Create expired message"""
    limit = len(content) if len(content) < limit else limit

    fridge_name = models.Fridges.objects.values("name").get(fridge_id=fridge_id)["name"]
    intro = f'Hey there! Your fridge {fridge_name} contains items, ' \
            f'which are going to expire in the next {due_in} days:'
    msg = [intro]
    c_msg = []
    for i in range(limit):
        entry = content[i]
        c_msg.append(f'{entry["item_count"]}x {entry["item__name"]}')
    msg.append(", ".join(c_msg))
    if len(content) > limit:
        rest = rest_amount(content[limit:])
        msg.append(f'and {rest} other items, which are about to expire as well.')
    msg.append("Check them out!")

    title = f"{fridge_name}: Items about to expire"
    return {"title": title, "body": "\n".join(msg)}


def rest_amount(content):
    """Count entries and return rest amount"""
    amount = 0
    for entry in content:
        amount += entry["item_count"]
    return amount
