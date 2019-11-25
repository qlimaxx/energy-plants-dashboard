import requests_mock
from django.conf import settings
from django.test import TestCase

from plants.utils import fetch_data_from_monitor, parse_data_from_monitor


MONITOR_RESPONSE = [{
    'datetime': '2019-01-01T{:02d}:00:00'.format(i),
    'expected': {'energy': 1, 'irradiation': 1},
    'observed': {'energy': 1, 'irradiation': 1}} for i in range(24)]


class UtilsTest(TestCase):

    @requests_mock.Mocker()
    def test_fetch_data_from_monitor(self, m):
        m.get(settings.MONITOR_URL, json=MONITOR_RESPONSE)
        result = fetch_data_from_monitor()
        self.assertEqual(result, MONITOR_RESPONSE)

    def test_parse_data_from_monitor(self):
        result = parse_data_from_monitor(MONITOR_RESPONSE)
        expected_result = [{'date': '2019-01-01', 'energy_expected': 1,
                            'energy_observed': 1, 'irradiation_expected': 1,
                            'irradiation_observed': 1}]
        self.assertEqual(result, expected_result)
