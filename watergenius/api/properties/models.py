from django.db import models

from api.models import Localization
from api.users.models import User


class Property(models.Model):
    prop_id = models.AutoField(primary_key=True)
    prop_name = models.CharField(max_length=50)
    prop_description = models.CharField(max_length=250)
    prop_address = models.CharField(max_length=100)
    prop_owner = models.ForeignKey(User, related_name='owned_by', on_delete=models.CASCADE)


class CentralNode(models.Model):
    node_id = models.AutoField(primary_key=True)
    node_ip = models.GenericIPAddressField()
    node_local = models.ForeignKey(Localization, related_name='is_in_local', on_delete=models.CASCADE)
    node_property = models.OneToOneField(Property, on_delete=models.CASCADE)
