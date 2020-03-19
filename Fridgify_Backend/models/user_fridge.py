from django.db import models


class UserFridge(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    fridge = models.ForeignKey('Fridges', on_delete=models.CASCADE)

    def __dir__(self):
        return ["id", "user", "fridge"]