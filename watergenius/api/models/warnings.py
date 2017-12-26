from django.db import models


class Warning(models.Model):
    warning_id = models.AutoField(primary_key=True)
    warning_description = models.CharField(max_length=300)