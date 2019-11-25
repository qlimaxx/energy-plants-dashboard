from rest_framework import serializers

from plants.models import DataPoint, Plant


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ('id', 'name')


class DataPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPoint
        fields = ('plant', 'date', 'energy_expected', 'energy_observed',
                  'irradiation_expected', 'irradiation_observed')
