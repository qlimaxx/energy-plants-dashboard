import mock
from django.test import TestCase

from plants.models import DataPoint, Plant
from plants.tasks import save_data_from_monitor


PLANT_NAME1 = 'Plant1'
PLANT_NAME2 = 'Plant2'
DATA = {'date': '2019-01-01', 'energy_expected': 1, 'energy_observed': 1,
        'irradiation_expected': 1, 'irradiation_observed': 1}


class TasksTest(TestCase):

    def setUp(self):
        self.plants = [
            Plant.objects.create(name=PLANT_NAME1),
            Plant.objects.create(name=PLANT_NAME2)]

    @mock.patch('plants.tasks.fetch_data_from_monitor', return_value=[])
    @mock.patch('plants.tasks.parse_data_from_monitor', return_value=[DATA])
    def test_save_data_from_monitor_with_new_data_from_monitor(
            self, fetch_data_from_monitor_func, parse_data_from_monitor_func):
        task = save_data_from_monitor.s().apply()
        self.assertEqual(task.status, 'SUCCESS')
        self.assertTrue(fetch_data_from_monitor_func.called)
        self.assertTrue(parse_data_from_monitor_func.called)
        self.assertEqual(DataPoint.objects.count(), 2)

    @mock.patch('plants.tasks.fetch_data_from_monitor', return_value=[])
    @mock.patch('plants.tasks.parse_data_from_monitor', return_value=[DATA])
    def test_save_data_from_monitor_with_existing_data_from_monitor(
            self, fetch_data_from_monitor_func, parse_data_from_monitor_func):
        DataPoint.objects.bulk_create([
            DataPoint(plant=self.plants[0], **DATA),
            DataPoint(plant=self.plants[1], **DATA)])
        self.assertEqual(DataPoint.objects.count(), 2)
        task = save_data_from_monitor.s().apply()
        self.assertEqual(task.status, 'SUCCESS')
        self.assertTrue(fetch_data_from_monitor_func.called)
        self.assertTrue(parse_data_from_monitor_func.called)
        self.assertEqual(DataPoint.objects.count(), 2)
