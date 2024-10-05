from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Item
from user.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class InventoryTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(first_name="milan", last_name="biranwar", location="pune",
                                             username='testuser', password='testpassword', email="newuser@example.com",
                                             mobile_num=918785220)
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.existing_item = Item.objects.create(
            name="Test Item", sku="TESTSKU123", quantity=10, price=100.0, description="A test item", category="Test Category"
        )

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_create_item(self):
        url = reverse('create_item')
        data = {
            "name": "New Item",
            "sku": "NEWSKU123",
            "quantity": 20,
            "price": 200.0,
            "description": "A new test item",
            "category": "New Category"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['Message'], 'Item created successfully')

    def test_create_item_duplicate_name(self):
        url = reverse('create_item')
        data = {
            "name": "Test Item",
            "sku": "DUPLICATESKU",
            "quantity": 5,
            "price": 50.0,
            "description": "Duplicate name test item",
            "category": "Duplicate Category"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Item with this name already exists', response.data['error'])

    def test_get_item(self):
        url = reverse('get_item', kwargs={'item_id': self.existing_item.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], self.existing_item.name)

    def test_get_item_not_found(self):
        url = reverse('get_item', kwargs={'item_id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Item not found', response.data['error'])

    def test_update_item(self):
        url = reverse('update_item', kwargs={'item_id': self.existing_item.id})
        data = {
            "name": "Updated Item",
            "sku": "UPDATEDSKU123",
            "quantity": 15,
            "price": 150.0,
            "description": "Updated item description",
            "category": "Updated Category"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Message'], 'Item updated successfully')
        self.assertEqual(response.data['data']['name'], 'Updated Item')

    def test_update_item_not_found(self):
        url = reverse('update_item', kwargs={'item_id': 999})
        data = {
            "name": "Non-existent Item",
            "sku": "NONEXISTSKU",
            "quantity": 0,
            "price": 0.0,
            "description": "Does not exist",
            "category": "None"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Item not found', response.data['error'])

    def test_delete_item(self):
        url = reverse('delete_item', kwargs={'item_id': self.existing_item.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_item_not_found(self):
        url = reverse('delete_item', kwargs={'item_id': 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Item not found', response.data['error'])
