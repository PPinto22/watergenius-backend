from django.db import models

from api.models.sensors import Sensor


# class ReadType(models.Model):
#     read_type_id = models.AutoField(primary_key=True)
#     read_type_name = models.CharField(max_length=50)
#     read_type_units = models.CharField(max_length=3)
#     read_type_coef = models.IntegerField()


class Read(models.Model):
    read_id = models.AutoField(primary_key=True)
    read_timestamp = models.DateTimeField(auto_now=True)
    read_value = models.FloatField()
    read_sensor = models.ForeignKey(Sensor, related_name='belongs_to_sensor', on_delete=models.CASCADE)
    # read_type = models.ForeignKey(ReadType, related_name='has_readtype', on_delete=models.CASCADE)
