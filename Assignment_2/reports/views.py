from django.shortcuts import render

# Create your views here.
# reports/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from items.models import Item
from purchases.models import PurchaseDetail
from sells.models import SellDetail
from datetime import datetime

class ItemStockReportView(APIView):
    """
    Generate a report on stock changes for a specific item within a date range
    """
    def get(self, request, item_code):
        # Get date parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        # Validate parameters
        if not start_date or not end_date:
            return Response(
                {"error": "Both start_date and end_date parameters are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"error": "Date format should be YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if item exists
        try:
            item = Item.objects.get(code=item_code, is_deleted=False)
        except Item.DoesNotExist:
            return Response(
                {"error": f"Item with code {item_code} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get all purchase details for this item in the date range
        purchase_details = PurchaseDetail.objects.filter(
            item__code=item_code,
            is_deleted=False,
            header__date__range=[start_date, end_date]
        ).select_related('header')
        
        # Get all sell details for this item in the date range
        sell_details = SellDetail.objects.filter(
            item__code=item_code,
            is_deleted=False,
            header__date__range=[start_date, end_date]
        ).select_related('header')
        
        # Calculate starting stock (stock at start_date)
        # This requires calculating all purchases and sells before start_date
        previous_purchases = PurchaseDetail.objects.filter(
            item__code=item_code,
            is_deleted=False,
            header__date__lt=start_date
        ).select_related('header')
        
        previous_sells = SellDetail.objects.filter(
            item__code=item_code,
            is_deleted=False,
            header__date__lt=start_date
        ).select_related('header')
        
        total_purchased_before = sum(pd.quantity for pd in previous_purchases)
        total_sold_before = sum(sd.quantity for sd in previous_sells)
        
        starting_stock = total_purchased_before - total_sold_before
        
        # Prepare chronological list of all transactions
        transactions = []
        
        for pd in purchase_details:
            transactions.append({
                'date': pd.header.date,
                'transaction_type': 'Purchase',
                'transaction_code': pd.header.code,
                'quantity': pd.quantity,
                'unit_price': float(pd.unit_price),
                'total_price': float(pd.quantity * pd.unit_price)
            })
        
        for sd in sell_details:
            transactions.append({
                'date': sd.header.date,
                'transaction_type': 'Sell',
                'transaction_code': sd.header.code,
                'quantity': -sd.quantity,  # Negative to show reduction
                'unit_price': None,  # We don't record sell price
                'total_price': None
            })
        
        # Sort transactions by date
        transactions.sort(key=lambda x: x['date'])
        
        # Calculate running balance
        running_stock = starting_stock
        for transaction in transactions:
            running_stock += transaction['quantity']
            transaction['running_stock'] = running_stock
        
        # Prepare report data
        report_data = {
            'item_code': item.code,
            'item_name': item.name,
            'start_date': start_date.strftime("%Y-%m-%d"),
            'end_date': end_date.strftime("%Y-%m-%d"),
            'starting_stock': starting_stock,
            'ending_stock': running_stock,
            'transactions': transactions
        }
        
        return Response(report_data)