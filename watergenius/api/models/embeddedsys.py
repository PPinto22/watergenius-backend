from django.db import models

from api.models.subspaces import SubSpace
from api.models.localizations import Localization

class EmbeddedSystem(models.Model):
    esys_id = models.AutoField(primary_key=True)
    esys_local = models.ForeignKey(Localization, related_name='is_in_localization', on_delete=models.CASCADE)
    esys_sub = models.ForeignKey(SubSpace, related_name='belongs_to_sub', on_delete=models.CASCADE)
    esys_state = models.IntegerField()
    esys_name = models.CharField(max_length=30, default="")
    esys_network_pass = models.CharField(max_length=30, default="")
