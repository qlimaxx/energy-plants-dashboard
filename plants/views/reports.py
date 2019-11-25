from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets

from plants.filters import DataPointFilter
from plants.models import DataPoint
from plants.serializers import DataPointSerializer


class ReportViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = DataPoint.objects.select_related('plant').order_by('date')
    serializer_class = DataPointSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DataPointFilter
