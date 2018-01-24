from django.db import models

from api.models.sensors import Sensor


class Read(models.Model):
    read_id = models.AutoField(primary_key=True)
    read_timestamp = models.DateTimeField(auto_now=True)
    read_value = models.FloatField()
    read_sensor = models.ForeignKey(Sensor, related_name='belongs_to_sensor', on_delete=models.CASCADE)
