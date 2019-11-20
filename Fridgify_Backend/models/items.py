from django.db import models


class Items(models.Model):
    item_id = models.AutoField(primary_key=True, unique=True)
    name = models.TextField()
    description = models.TextField()
    store = models.ForeignKey("Stores", on_delete=models.CASCADE)
