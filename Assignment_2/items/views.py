from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Item instances.
    """
    queryset = Item.objects.filter(is_deleted=False)
    serializer_class = ItemSerializer
    lookup_field = 'code'

    def get_queryset(self):
        """
        This view should return a list of all items that aren't deleted.
        """
        return Item.objects.filter(is_deleted=False)

    def destroy(self, request, *args, **kwargs):
        """
        Implement soft delete by setting is_deleted flag to True
        """
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)