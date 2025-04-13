# reports/urls.py
from django.urls import path
from .views import ItemStockReportView

urlpatterns = [
    path('report/<str:item_code>/', ItemStockReportView.as_view(), name='item-stock-report'),
]