import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Plant(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class DataPoint(BaseModel):
    energy_expected = models.FloatField()
    energy_observed = models.FloatField()
    irradiation_expected = models.FloatField()
    irradiation_observed = models.FloatField()
    date = models.DateField()
    plant = models.ForeignKey(
        Plant, related_name='data_points', on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.plant, self.date)
