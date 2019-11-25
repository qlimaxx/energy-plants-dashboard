from rest_framework import viewsets

from plants.models import Plant
from plants.serializers import PlantSerializer


class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
