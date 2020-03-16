from django.db import models


class Fridges(models.Model):
    fridge_id = models.AutoField(primary_key=True, unique=True)
    name = models.TextField()
    description = models.TextField(null=True)

    def __dir__(self):
        return ["fridge_id", "name", "description"]
