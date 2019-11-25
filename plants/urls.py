from django.urls import path
from rest_framework import routers

from plants.views import home, monitor, plants, reports


app_name = 'plants'

router = routers.SimpleRouter()
router.register(r'plants', plants.PlantViewSet, basename='plants')
router.register(r'reports', reports.ReportViewSet, basename='reports')

urlpatterns = router.urls + [
    path('', home.index, name='home'),
    path('monitor/pull/', monitor.pull_data, name='pull-data'),
]
