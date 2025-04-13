# purchases/models.py
from django.db import models
from models import BaseModel  # Changed from warehouse_system.models import BaseModel
from items.models import Item
from decimal import Decimal

class PurchaseHeader(BaseModel):
    """
    Model representing purchase headers/transactions
    """
    code = models.CharField(max_length=20, unique=True)
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Purchase {self.code} - {self.date}"

class PurchaseDetail(BaseModel):
    """
    Model representing line items in a purchase transaction
    """
    header = models.ForeignKey(PurchaseHeader, on_delete=models.CASCADE, related_name='details')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, to_field='code')
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.header.code} - {self.item.code} - {self.quantity}"

    def save(self, *args, **kwargs):
        """
        Override save method to update item stock and balance
        """
        # Check if this is a new record
        is_new = self._state.adding
        
        super().save(*args, **kwargs)
        
        # Only update stock and balance for new records to avoid duplicate updates
        if is_new:
            # Update the item's stock and balance
            item = self.item
            item.stock += self.quantity
            item.balance += Decimal(self.quantity) * self.unit_price
            item.save()