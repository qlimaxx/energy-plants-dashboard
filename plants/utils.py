import time
from collections import defaultdict
from functools import wraps

import requests
from django.conf import settings

from plants.exceptions import NoAvailableDataError


def retry(exception, tries=3, delay=1, backoff=2):
    def decorator(f):
        @wraps(f)
        def do_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exception:
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)
        return do_retry
    return decorator


@retry(NoAvailableDataError)
def fetch_data_from_monitor(params=None, timeout=30):
    data = requests.get(
        settings.MONITOR_URL, timeout=timeout, params=params).json()
    if 'error' in data:
        raise NoAvailableDataError
    return data


def parse_data_from_monitor(data):
    parsed = []
    dates = defaultdict(lambda: {'count': 0, 'data': defaultdict(int)})
    for e in data:
        date = e['datetime'].split('T')[0]
        dates[date]['count'] += 1
        dates[date]['data']['energy_expected'] += e['expected']['energy']
        dates[date]['data']['energy_observed'] += e['observed']['energy']
        dates[date]['data']['irradiation_expected'] += e['expected']['irradiation']
        dates[date]['data']['irradiation_observed'] += e['observed']['irradiation']
    for date, e in dates.items():
        for k, v in e['data'].items():
            e['data'][k] = v / e['count']
        d = {'date': date}
        d.update(e['data'])
        parsed.append(d)
    return parsed
