"""
Model representation for Items
"""

from django.db import models
from rest_framework import serializers


class Items(models.Model):
    """
    Stores all existing items with a related :model:`store.Stores`
    """
    item_id = models.AutoField(primary_key=True, unique=True)
    barcode = models.TextField(default="")
    name = models.TextField()
    description = models.TextField()
    store = models.ForeignKey("Stores", on_delete=models.CASCADE)

    def __dir__(self):
        return ["item_id", "barcode", "name", "description", "store"]


class ItemsSerializer(serializers.ModelSerializer):
    """
    Serialize Items
    """
    class Meta:
        # pylint: disable=too-few-public-methods, missing-class-docstring
        model = Items
        fields = "__all__"
