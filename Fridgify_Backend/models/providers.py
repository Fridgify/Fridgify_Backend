from django.db import models


class Providers(models.Model):
    provider_id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255, unique=True)

    def __dir__(self):
        return ["provider_id", "name"]
