from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from plants.models import DataPoint, Plant


PLANT_NAME1 = 'Plant1'
PLANT_NAME2 = 'Plant2'


class ReportViewSetTestCase(APITestCase):

    def setUp(self):
        self.plants = [
            Plant.objects.create(name=PLANT_NAME1),
            Plant.objects.create(name=PLANT_NAME2)]
        data = {'energy_expected': 1, 'energy_observed': 1,
                'irradiation_expected': 1, 'irradiation_observed': 1}
        self.data_points = [
            DataPoint(plant=self.plants[0], date='2019-01-01', **data),
            DataPoint(plant=self.plants[0], date='2019-01-02', **data),
            DataPoint(plant=self.plants[0], date='2019-01-03', **data),
            DataPoint(plant=self.plants[1], date='2019-01-01', **data),
            DataPoint(plant=self.plants[1], date='2019-01-02', **data)]
        DataPoint.objects.bulk_create(self.data_points)

    def test_list_datapoints(self):
        response = self.client.get(reverse('plants:reports-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), len(self.data_points))

    def test_filter_datapoints_by_plant(self):
        response = self.client.get(
            reverse('plants:reports-list'), {'plant': self.plants[0].id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)

    def test_filter_datapoints_by_date(self):
        response = self.client.get(
            reverse('plants:reports-list'), {'date_from': '2019-01-02'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)
