from django_filters import rest_framework as filters

from plants.models import DataPoint


class DataPointFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = DataPoint
        fields = ('plant', 'date_from', 'date_to')
