from django.db import models

from api.spaces.models import Space


class SubSpace(models.Model):
    sub = models.AutoField(primary_key=True)
    sub_name = models.CharField(max_length=50)
    sub_description = models.CharField(max_length=150)
    sub_space_id = models.ForeignKey(Space, related_name='belongs_to_space', on_delete=models.CASCADE)
