# items/serializers.py
from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['code', 'name', 'unit', 'description', 'stock', 'balance', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'stock', 'balance']