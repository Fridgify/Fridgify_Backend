from django.db import models


class Items(models.Model):
    item_id = models.AutoField(primary_key=True, unique=True)
    barcode = models.TextField(default="")
    name = models.TextField()
    description = models.TextField()
    store = models.ForeignKey("Stores", on_delete=models.CASCADE)

    def __dir__(self):
        return ["item_id", "barcode", "name", "description", "store"]
