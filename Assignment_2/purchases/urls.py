# purchases/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PurchaseHeaderViewSet

router = DefaultRouter()
router.register(r'purchase', PurchaseHeaderViewSet, basename='purchase')

urlpatterns = [
    path('', include(router.urls)),
]