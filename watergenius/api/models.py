from django.db import models

class Localization(models.Model):
    local_id = models.AutoField(primary_key=True)
    local_long = models.FloatField()
    local_lat = models.FloatField()
