# items/models.py
from django.db import models
from models import BaseModel  # Changed from warehouse_system.models import BaseModel

class Item(BaseModel):
    """
    Model representing warehouse items with stock and financial tracking
    """
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    stock = models.IntegerField(default=0)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.code} - {self.name}"