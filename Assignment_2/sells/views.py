# sells/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SellHeader, SellDetail
from .serializers import (
    SellHeaderSerializer, 
    SellHeaderCreateSerializer,
    SellDetailSerializer,
    SellDetailCreateSerializer
)

class SellHeaderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing SellHeader instances.
    """
    queryset = SellHeader.objects.filter(is_deleted=False)
    lookup_field = 'code'
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SellHeaderCreateSerializer
        return SellHeaderSerializer
    
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
        Retrieve all details for a specific sell header
        """
        sell = self.get_object()
        details = SellDetail.objects.filter(header=sell, is_deleted=False)
        serializer = SellDetailSerializer(details, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def details(self, request, code=None):
        """
        Create a new detail for a specific sell header
        """
        sell = self.get_object()
        serializer = SellDetailCreateSerializer(
            data=request.data,
            context={'header_code': code}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
