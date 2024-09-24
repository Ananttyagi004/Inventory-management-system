from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Item

class ItemManagementTests(APITestCase):
    def setUp(self):
        self.item_url = reverse('item-list')  # Adjust to your URL name for listing items
        self.item_detail_url = lambda sku: reverse('item-detail', kwargs={'sku': sku})  # Adjust for detail view
        self.item_data = {
            "sku": "SKU00123",
            "name": "Wireless Bluetooth Headphones",
            "description": "High-quality wireless headphones with noise cancellation."
        }
        self.create_item()

    def create_item(self):
        self.client.post(self.item_url, self.item_data, format='json')

    def test_create_item(self):
        response = self.client.post(self.item_url, self.item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)  # Check if item count increased

    def test_read_item(self):
        response = self.client.get(self.item_detail_url("SKU00123"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item_data['name'])

    def test_update_item(self):
        updated_data = {
            "sku": "SKU00123",
            "name": "Wireless Bluetooth Headphones Pro",
            "description": "Updated version with improved noise cancellation."
        }
        response = self.client.put(self.item_detail_url("SKU00123"), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['item']['name'], updated_data['name'])

    def test_delete_item(self):
        response = self.client.delete(self.item_detail_url("SKU00123"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.count(), 0)  # Ensure item count is zero after deletion

    def test_read_nonexistent_item(self):
        response = self.client.get(self.item_detail_url("NONEXISTENTSKU"))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('errors', response.data)

