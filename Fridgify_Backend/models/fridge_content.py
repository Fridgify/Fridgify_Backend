import uuid

from django.db import models
from rest_framework import serializers


class FridgeContent(models.Model):
    """
    Stores :model:`item.Items` of a :model:`fridge.Fridges`
    """
    id = models.AutoField(primary_key=True)
    fridge = models.ForeignKey('Fridges', on_delete=models.CASCADE)
    item = models.ForeignKey('Items', on_delete=models.CASCADE)
    content_id = models.UUIDField(default=uuid.uuid4, editable=False)
    amount = models.IntegerField(default=1)
    max_amount = models.IntegerField(default=1)
    expiration_date = models.DateTimeField()
    unit = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('fridge', 'content_id'))

    def __dir__(self):
        return [
            "id", "fridge", "item", "amount", "expiration_date", "unit", "created_at", "last_updated"
        ]


class FridgeContentSerializer(serializers.ModelSerializer):
    expiration_date = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = FridgeContent
        fields = '__all__'


class FridgeContentItemSerializer(serializers.ModelSerializer):
    expiration_date = serializers.DateTimeField(format="%Y-%m-%d")
    item = serializers.CharField(source="content_id")

    class Meta:
        model = FridgeContent
        fields = ("item", "fridge", "max_amount", "amount", "unit", "expiration_date", "created_at")