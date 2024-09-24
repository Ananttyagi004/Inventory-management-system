from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.conf import settings
from .models import Item
from .serializers import  ItemSerializer
from rest_framework.permissions import IsAuthenticated
import logging

logger = logging.getLogger('inventory_management')
CACHE_TTL=60*15

class ItemView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Item {serializer.data['sku']} created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Item creation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, sku):
        cache_key = f"item_{sku}"
        cached_item = cache.get(cache_key)

        if cached_item:
            logger.info(f"Item {sku} retrieved from cache")
            return Response(cached_item, status=status.HTTP_200_OK)

        try:
            item = Item.objects.get(sku=sku)
            logger.info(f"Item {sku} retrieved from database")
        except Item.DoesNotExist:
            logger.error(f"Item {sku} not found")
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(item)
        cache.set(cache_key, serializer.data, timeout=CACHE_TTL)
        logger.info(f"Item {sku} stored in cache")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, sku):
        try:
            item = Item.objects.get(sku=sku)
        except Item.DoesNotExist:
            logger.error(f"Item {sku} not found for update")
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache_key = f"item_{sku}"
            cache.set(cache_key, serializer.data, timeout=CACHE_TTL)
            logger.info(f"Item {sku} updated and cache refreshed")
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.error(f"Item update failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, sku):
        try:
            item = Item.objects.get(sku=sku)
        except Item.DoesNotExist:
            logger.error(f"Item {sku} not found for deletion")
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        item.delete()
        cache_key = f"item_{sku}"
        cache.delete(cache_key)
        logger.info(f"Item {sku} deleted and cache invalidated")
        return Response({'message': 'Item deleted successfully'}, status=status.HTTP_200_OK)


