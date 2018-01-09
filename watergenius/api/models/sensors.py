from django.db import models

from api.models.embeddedsys import EmbeddedSystem


class SensorType(models.Model):
    sensor_type_id = models.AutoField(primary_key=True)
    sensor_type_name = models.CharField(max_length=50)


class Sensor(models.Model):
    sensor_id = models.AutoField(primary_key=True)
    sensor_name = models.CharField(max_length=50, default="sensor nr x")
    sensor_state = models.IntegerField()
    sensor_sub = models.ForeignKey(EmbeddedSystem, related_name='belongs_to_embsys', on_delete=models.CASCADE)
    sensor_timerate = models.IntegerField()
    sensor_depth = models.IntegerField()
    sensor_type = models.ForeignKey(SensorType, related_name='has_type', on_delete=models.CASCADE)
