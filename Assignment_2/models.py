# Create a new file: warehouse_system/models.py

from django.db import models

class BaseModel(models.Model):
    """
    Abstract base model providing common fields for all models
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True