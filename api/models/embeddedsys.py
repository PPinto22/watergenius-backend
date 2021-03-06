from django.db import models

from api.models.subspaces import SubSpace


class EmbeddedSystem(models.Model):
    esys_id = models.AutoField(primary_key=True)
    esys_local_lat = models.FloatField(default=0)
    esys_local_long = models.FloatField(default=0)
    esys_local_alt = models.FloatField(default=0)
    esys_sub = models.ForeignKey(SubSpace, related_name='belongs_to_sub', on_delete=models.CASCADE)
    #esys_state = models.IntegerField()
    esys_last_read =  models.DateTimeField(auto_now=True)
    esys_name = models.CharField(max_length=30, default="")
