from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from plants.models import Plant


PLANT_NAME1 = 'Plant1'
PLANT_NAME2 = 'Plant2'


class PlantViewSetTestCase(APITestCase):

    def test_list_plants(self):
        Plant.objects.create(name=PLANT_NAME1)
        Plant.objects.create(name=PLANT_NAME2)
        response = self.client.get(reverse('plants:plants-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_create_plant(self):
        response = self.client.post(
            reverse('plants:plants-list'), {'name': PLANT_NAME1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(Plant.objects.get(name=PLANT_NAME1))

    def test_read_plant(self):
        plant = Plant.objects.create(name=PLANT_NAME1)
        response = self.client.get(
            reverse('plants:plants-detail', args=(plant.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], PLANT_NAME1)

    def test_update_plant(self):
        plant = Plant.objects.create(name=PLANT_NAME1)
        response = self.client.put(
            reverse('plants:plants-detail', args=(plant.id,)), {'name': PLANT_NAME2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        plant.refresh_from_db()
        self.assertEqual(plant.name, PLANT_NAME2)

    def test_delete_plant(self):
        plant = Plant.objects.create(name=PLANT_NAME1)
        response = self.client.delete(
            reverse('plants:plants-detail', args=(plant.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Plant.DoesNotExist):
            Plant.objects.get(id=plant.id)
