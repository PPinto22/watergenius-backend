from django.db import models
from api.models.properties import Property

class Warning(models.Model):
    warning_id = models.AutoField(primary_key=True)
    warning_description = models.CharField(max_length=300)
    warning_property = models.ForeignKey(Property, related_name='refer_property', on_delete=models.CASCADE)