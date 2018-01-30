from django.db import models

from api.models.embeddedsys import EmbeddedSystem


class SensorType(models.Model):
    # id = sensor_type_name_eng
    sensor_type_id = models.CharField(primary_key=True, max_length=50)
    sensor_type_name_eng = models.CharField(max_length=50, default="")
    sensor_type_name_por = models.CharField(max_length=50, default="")
    sensor_type_unit = models.CharField(max_length=10, default="")


class Sensor(models.Model):
    sensor_id = models.AutoField(primary_key=True)
    sensor_name = models.CharField(max_length=50, default="")
    #sensor_state = models.IntegerField()
    sensor_last_read = models.DateTimeField(auto_now=True)
    sensor_esys = models.ForeignKey(EmbeddedSystem, related_name='belongs_to_embsys', on_delete=models.CASCADE)
    sensor_timerate = models.IntegerField(default=30)
    sensor_timerate_unit = models.CharField(max_length=6, default="min")
    sensor_depth = models.IntegerField()
    sensor_depth_unit = models.CharField(max_length=6, default="cm")
    sensor_type = models.ForeignKey(SensorType, related_name='has_type', on_delete=models.CASCADE)
