# sells/serializers.py
from rest_framework import serializers
from .models import SellHeader, SellDetail
from items.models import Item
from django.core.exceptions import ValidationError

class SellDetailSerializer(serializers.ModelSerializer):
    item_code = serializers.CharField(source='item.code', read_only=True)
    header_code = serializers.CharField(source='header.code', read_only=True)
    
    class Meta:
        model = SellDetail
        fields = ['id', 'item_code', 'quantity', 'header_code', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class SellDetailCreateSerializer(serializers.ModelSerializer):
    item_code = serializers.CharField(write_only=True)
    
    class Meta:
        model = SellDetail
        fields = ['item_code', 'quantity']
    
    def validate(self, data):
        """
        Check that there's enough stock for the sell
        """
        item_code = data.get('item_code')
        quantity = data.get('quantity')
        
        try:
            item = Item.objects.get(code=item_code)
            if quantity > item.stock:
                raise serializers.ValidationError(f"Not enough stock for item {item_code}. Available: {item.stock}, Requested: {quantity}")
        except Item.DoesNotExist:
            raise serializers.ValidationError(f"Item with code {item_code} does not exist")
        
        return data
    
    def create(self, validated_data):
        item_code = validated_data.pop('item_code')
        header_code = self.context.get('header_code')
        
        try:
            item = Item.objects.get(code=item_code)
            header = SellHeader.objects.get(code=header_code)
        except (Item.DoesNotExist, SellHeader.DoesNotExist):
            raise serializers.ValidationError("Invalid item_code or header_code")
        
        sell_detail = SellDetail.objects.create(
            item=item,
            header=header,
            **validated_data
        )
        
        return sell_detail

class SellHeaderSerializer(serializers.ModelSerializer):
    details = SellDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = SellHeader
        fields = ['code', 'date', 'description', 'details', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class SellHeaderCreateSerializer(serializers.ModelSerializer):
    details = SellDetailCreateSerializer(many=True, required=False)
    
    class Meta:
        model = SellHeader
        fields = ['code', 'date', 'description', 'details']
    
    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        sell_header = SellHeader.objects.create(**validated_data)
        
        for detail_data in details_data:
            item_code = detail_data.pop('item_code')
            try:
                item = Item.objects.get(code=item_code)
                
                # Validate stock availability
                if detail_data['quantity'] > item.stock:
                    raise serializers.ValidationError(
                        f"Not enough stock for item {item_code}. Available: {item.stock}, Requested: {detail_data['quantity']}"
                    )
                
                SellDetail.objects.create(
                    header=sell_header,
                    item=item,
                    **detail_data
                )
            except Item.DoesNotExist:
                raise serializers.ValidationError(f"Item with code {item_code} does not exist")
        
        return sell_header