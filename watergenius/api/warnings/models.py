from django.db import models

from api.subspaces.models import SubSpace

class Warnings(models.Model):
    warning_id = models.AutoField(primary_key=True)
    warning_description = models.CharField(max_length=300)