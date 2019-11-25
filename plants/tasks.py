from __future__ import absolute_import, unicode_literals

import datetime

from celery.utils.log import get_task_logger

from plants.exceptions import NoAvailableDataError
from plants.models import DataPoint, Plant
from plants.utils import fetch_data_from_monitor, parse_data_from_monitor
from projconf.celery import app


logger = get_task_logger(__name__)


@app.task
def save_data_from_monitor(plant=None, date_from=None, date_to=None):
    logger.info('Starting updating data from monitor')
    if plant:
        plants = Plant.objects.filter(id=plant)
    else:
        plants = Plant.objects.all()
    if not date_from:
        date_from = datetime.date.today().strftime('%Y-%m-%d')
    if not date_to:
        date_to = (datetime.date.today() +
                   datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    for p in plants:
        try:
            data = fetch_data_from_monitor(
                params={'plant-id': p.id, 'from': date_from, 'to': date_to})
        except NoAvailableDataError:
            continue
        parsed = parse_data_from_monitor(data)
        for elem in parsed:
            DataPoint.objects.update_or_create(
                plant=p, date=elem['date'], defaults=elem)
    logger.info('Updating data is completed')
