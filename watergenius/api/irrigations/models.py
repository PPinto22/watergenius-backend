from django.db import models

from api.subspaces.models import SubSpace


class IrrigationTime(models.Model):
    irrigation_time_id = models.AutoField(primary_key=True)
    irrigation_time_date = models.DateTimeField()
    irrigation_time_qtd = models.IntegerField()
    irrigation_time_sub = models.ForeignKey(SubSpace, related_name='refers_to', on_delete=models.CASCADE)
