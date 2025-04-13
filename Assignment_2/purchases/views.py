# purchases/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PurchaseHeader, PurchaseDetail
from .serializers import (
    PurchaseHeaderSerializer, 
    PurchaseHeaderCreateSerializer,
    PurchaseDetailSerializer,
    PurchaseDetailCreateSerializer
)

class PurchaseHeaderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing PurchaseHeader instances.
    """
    queryset = PurchaseHeader.objects.filter(is_deleted=False)
    lookup_field = 'code'
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PurchaseHeaderCreateSerializer
        return PurchaseHeaderSerializer
    
    def destroy(self, request, *args, **kwargs):
        """
        Implement soft delete by setting is_deleted flag to True
        """
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        # Also mark all associated details as deleted
        instance.details.all().update(is_deleted=True)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'])
    def details(self, request, code=None):
        """
        Retrieve all details for a specific purchase header
        """
        purchase = self.get_object()
        details = PurchaseDetail.objects.filter(header=purchase, is_deleted=False)
        serializer = PurchaseDetailSerializer(details, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def details(self, request, code=None):
        """
        Create a new detail for a specific purchase header
        """
        purchase = self.get_object()
        serializer = PurchaseDetailCreateSerializer(
            data=request.data,
            context={'header_code': code}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)