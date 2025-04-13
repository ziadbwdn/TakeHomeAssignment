from django.db import models
from models import BaseModel  # Changed from warehouse_system.models import BaseModel
from items.models import Item
from decimal import Decimal
from django.core.exceptions import ValidationError

class SellHeader(BaseModel):
    """
    Model representing sell headers/transactions
    """
    code = models.CharField(max_length=20, unique=True)
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Sell {self.code} - {self.date}"

class SellDetail(BaseModel):
    """
    Model representing line items in a sell transaction
    """
    header = models.ForeignKey(SellHeader, on_delete=models.CASCADE, related_name='details')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, to_field='code')
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.header.code} - {self.item.code} - {self.quantity}"

    def clean(self):
        """
        Validate that there's enough stock to sell
        """
        if self.quantity > self.item.stock:
            raise ValidationError(f"Not enough stock for item {self.item.code}. Available: {self.item.stock}, Requested: {self.quantity}")

    def save(self, *args, **kwargs):
        """
        Override save method to update item stock and balance
        """
        # Check if this is a new record
        is_new = self._state.adding
        
        # Validate there's enough stock
        self.clean()
        
        super().save(*args, **kwargs)
        
        # Only update stock and balance for new records to avoid duplicate updates
        if is_new:
            # Update the item's stock and calculate balance reduction
            item = self.item
            
            # Calculate average unit cost for the sold items
            avg_unit_cost = Decimal('0.00')
            if item.stock > 0:
                avg_unit_cost = item.balance / Decimal(item.stock)
            
            # Update stock and balance
            balance_reduction = Decimal(self.quantity) * avg_unit_cost
            
            item.stock -= self.quantity
            item.balance -= balance_reduction
            item.save()