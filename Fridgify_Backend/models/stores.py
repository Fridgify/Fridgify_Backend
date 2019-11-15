from django.db import models


class Stores(models.Model):
    store_id = models.AutoField(primary_key=True, unique=True)
    name = models.TextField()
