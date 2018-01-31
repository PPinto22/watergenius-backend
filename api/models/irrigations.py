from django.db import models

from api.models.subspaces import SubSpace


class IrrigationTime(models.Model):
    irrigation_time_id = models.AutoField(primary_key=True)
    irrigation_time_date = models.DateTimeField()
    irrigation_time_qty = models.FloatField()
    irrigation_time_qty_unit = models.CharField(max_length=10, default='mm')
    irrigation_time_sub = models.ForeignKey(SubSpace, related_name='refers_to', on_delete=models.CASCADE)
