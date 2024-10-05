from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    sku = models.CharField(max_length=50, unique=True, db_index=True)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=100)

