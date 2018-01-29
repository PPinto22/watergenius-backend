from django.db import models
from django.utils.timezone import now

from api.models.sensors import Sensor


class Read(models.Model):
    read_id = models.AutoField(primary_key=True)
    read_timestamp = models.DateTimeField(default=now)
    read_value = models.FloatField()
    read_sensor = models.ForeignKey(Sensor, related_name='belongs_to_sensor', on_delete=models.CASCADE)
