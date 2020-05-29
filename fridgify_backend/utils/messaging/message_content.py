import itertools

from django.db.models import Count, F
from django.utils import timezone

from fridgify_backend import models
from fridgify_backend.utils import const


def get_grouped_content(due_in):
    content = models.FridgeContent.objects.values(
        "item_id",
        "item__name",
        "fridge_id",
    ).annotate(
        item_count=Count("item_id")
    ).filter(
        expiration_date__range=[F("expiration_date") - timezone.timedelta(days=due_in), F("expiration_date")],
    ).order_by("fridge_id", "item_id")

    return [(key, list(value)) for key, value in itertools.groupby(content, key=lambda entry: entry["fridge_id"])]


def get_recipients(fridge_id):
    users = models.UserFridge.objects.values_list("user_id").filter(fridge_id=fridge_id)
    user_ids = [user[0] for user in users]

    tokens = models.Accesstokens.objects.values_list("accesstoken", "provider_id").filter(
        user_id__in=user_ids,
        provider_id__in=const.Constants.NOTIFICATION_SERVICES
    ).order_by("provider_id")

    recipients_dict = {}
    for key, value in itertools.groupby(tokens, key=lambda entry: entry[1]):
        recipients_dict[key] = [x[0] for x in value]

    return recipients_dict


def create_expired_message(fridge_id, content, due_in, limit=3):
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
    rest = rest_amount(content[len(content)-limit:])
    msg.append(f'and {rest} other items, which are about to expire as well. Check them out!')

    title = f"{fridge_name}: Items about to expire"
    return {"title": title, "body": "\n".join(msg)}


def rest_amount(content):
    amount = 0
    for entry in content:
        amount += entry["item_count"]
    return amount
