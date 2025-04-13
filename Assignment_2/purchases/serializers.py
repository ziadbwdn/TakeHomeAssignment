# purchases/serializers.py
from rest_framework import serializers
from .models import PurchaseHeader, PurchaseDetail
from items.models import Item

class PurchaseDetailSerializer(serializers.ModelSerializer):
    item_code = serializers.CharField(source='item.code', read_only=True)
    header_code = serializers.CharField(source='header.code', read_only=True)
    
    class Meta:
        model = PurchaseDetail
        fields = ['id', 'item_code', 'quantity', 'unit_price', 'header_code', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class PurchaseDetailCreateSerializer(serializers.ModelSerializer):
    item_code = serializers.CharField(write_only=True)
    
    class Meta:
        model = PurchaseDetail
        fields = ['item_code', 'quantity', 'unit_price']
    
    def create(self, validated_data):
        item_code = validated_data.pop('item_code')
        header_code = self.context.get('header_code')
        
        try:
            item = Item.objects.get(code=item_code)
            header = PurchaseHeader.objects.get(code=header_code)
        except (Item.DoesNotExist, PurchaseHeader.DoesNotExist):
            raise serializers.ValidationError("Invalid item_code or header_code")
        
        purchase_detail = PurchaseDetail.objects.create(
            item=item,
            header=header,
            **validated_data
        )
        
        return purchase_detail

class PurchaseHeaderSerializer(serializers.ModelSerializer):
    details = PurchaseDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = PurchaseHeader
        fields = ['code', 'date', 'description', 'details', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class PurchaseHeaderCreateSerializer(serializers.ModelSerializer):
    details = PurchaseDetailCreateSerializer(many=True, required=False)
    
    class Meta:
        model = PurchaseHeader
        fields = ['code', 'date', 'description', 'details']
    
    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        purchase_header = PurchaseHeader.objects.create(**validated_data)
        
        for detail_data in details_data:
            item_code = detail_data.pop('item_code')
            try:
                item = Item.objects.get(code=item_code)
                PurchaseDetail.objects.create(
                    header=purchase_header,
                    item=item,
                    **detail_data
                )
            except Item.DoesNotExist:
                raise serializers.ValidationError(f"Item with code {item_code} does not exist")
        
        return purchase_header