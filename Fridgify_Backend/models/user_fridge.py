from django.db import models


class UserFridge(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE)
    fridge_id = models.ForeignKey('Fridges', on_delete=models.CASCADE)
