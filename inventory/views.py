from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Item
from .serializers import ItemSerializer
import logging
from django.core.cache import cache
from django.conf import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 5)


logging.basicConfig(filename='inventory.log',
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_item(request):
    name = request.data.get('name')
    sku = request.data.get('sku')

    if Item.objects.filter(name=name).exists():
        return Response({"error": "Item with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)

    if Item.objects.filter(sku=sku).exists():
        return Response({"error": "Item with this SKU already exists"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            logging.info(f"Item created: {serializer.data['name']}")
            return Response({"Message": "Item created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(f"Error creating item: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Handle validation errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_item(request, item_id):
    cache_key = f'item_{item_id}'
    cached_item = cache.get(cache_key)

    if cached_item:
        logging.info(f"Item retrieved from cache: {cached_item['name']}")
        return Response({"Message": "Item retrieved successfully", "data": cached_item})

    try:
        item = Item.objects.get(id=item_id)
        serializer = ItemSerializer(item)
        logging.info(f"Item retrieved from database: {serializer.data['name']}")

        cache.set(cache_key, serializer.data, timeout=CACHE_TTL)
        return Response({"Message": "Item retrieved successfully", "data": serializer.data})
    except Item.DoesNotExist:
        logging.error(f"Item with ID {item_id} not found")
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        logging.error(f"Item with ID {item_id} not found")
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ItemSerializer(item, data=request.data)
    if serializer.is_valid():
        serializer.save()
        logging.info(f"Item updated: {serializer.data['name']}")
        return Response({"Message": "Item updated successfully", "data": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        item.delete()
        logging.info(f"Item deleted: {item.name}")
        return Response({'message': 'Item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Item.DoesNotExist:
        logging.error(f"Item with ID {item_id} not found")
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
