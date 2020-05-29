from django.db.models import Count, When, Case, IntegerField, Q
from django.db import models
from django.utils import timezone

from fridgify_backend.models import FridgeContent


def non_unique_keys(request_body, model, *args):
    keys = []
    for unique_key in args:
        if model.objects.filter(**{unique_key: request_body[unique_key]}).exists():
            keys.append(unique_key)
    return keys


def get_content(user, fridge_id=None):
    db_filter = {"fridge__userfridge__user": user}
    if fridge_id is not None:
        db_filter["fridge_id"]: fridge_id

    content = FridgeContent.objects.values(
        "fridge_id",
    ).annotate(
        total=Count("item_id"),
        fresh=Count(Case(
            When(expiration_date__gt=timezone.now() + timezone.timedelta(5), then=1),
            output_field=IntegerField()
        )),
        dueSoon=Count(Case(
            When(
                Q(expiration_date__gte=timezone.now()) & Q(expiration_date__lte=timezone.now() + timezone.timedelta(5)),
                then=1
            ),
            output_field=IntegerField()
        )),
        overDue=Count(Case(
            When(expiration_date__lt=timezone.now(), then=1),
            output_field=IntegerField()
        )),
    ).filter(**db_filter).order_by("fridge_id")

    return content
