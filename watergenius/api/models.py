from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models


# from django.contrib.gis.db import models as modelos - geo cordinates


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True, db_index=True, primary_key=True)
    USERNAME_FIELD = 'email'
    first_name = models.CharField(max_length=20, default="")
    last_name =models.CharField(max_length=20, default="")
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    props = models.ManyToManyField('Property', through='UserHasProperty')
    objects = UserManager()

    def __str__(self):
        return 'email -> ' + self.email + ' Name -> ' + self.first_name + " " + self.last_name


class Property(models.Model):
    prop_id = models.AutoField(primary_key=True)
    prop_name = models.CharField(max_length=50)
    prop_description = models.CharField(max_length=250)
    prop_address = models.CharField(max_length=100)
    prop_owner = models.ForeignKey(User, related_name='owned_by', on_delete=models.CASCADE)


class UserHasProperty(models.Model):
    user_has_id = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    prop_has_id = models.ForeignKey(Property, related_name='prop', on_delete=models.CASCADE)


class PlantType(models.Model):
    plant_type_id = models.AutoField(primary_key=True)
    plant_type_name = models.CharField(max_length=50)


class Space(models.Model):
    space_id = models.AutoField(primary_key=True)
    space_name = models.CharField(max_length=50)
    space_description = models.CharField(max_length=150)
    space_irrigation_hour = models.IntegerField()
    space_property = models.ForeignKey(Property, related_name='belongs_to_property', on_delete=models.CASCADE)
    space_plant_type = models.ForeignKey(PlantType, related_name='has_plant_type', on_delete=models.CASCADE)


class TimeRestrition(models.Model):
    time_restrition_id = models.AutoField(primary_key=True)
    time_begin = models.DateTimeField()
    time_duration = models.DurationField()
    time_restrition_space = models.ForeignKey(Space, related_name='belongs_to_spaceid', on_delete=models.CASCADE)


class Localization(models.Model):
    local_id = models.AutoField(primary_key=True)
    local_long = models.FloatField()
    local_lat = models.FloatField()


class CentralNode(models.Model):
    node_id = models.AutoField(primary_key=True)
    node_ip = models.GenericIPAddressField()
    node_local = models.ForeignKey(Localization, related_name='is_in_local', on_delete=models.CASCADE)


class SubSpace(models.Model):
    sub = models.AutoField(primary_key=True)
    sub_name = models.CharField(max_length=50)
    sub_description = models.CharField(max_length=150)
    sub_space_id = models.ForeignKey(Space, related_name='belongs_to_space', on_delete=models.CASCADE)


class EmbeddedSystem(models.Model):
    esys_id = models.AutoField(primary_key=True)
    esys_local = models.ForeignKey(Localization, related_name='is_in_localization', on_delete=models.CASCADE)
    esys_sub = models.ForeignKey(SubSpace, related_name='belongs_to_sub', on_delete=models.CASCADE)
    esys_state = models.IntegerField()


class SensorType(models.Model):
    sensor_type_id = models.AutoField(primary_key=True)
    sensor_type_name = models.CharField(max_length=50)


class Sensor(models.Model):
    sensor_id = models.AutoField(primary_key=True)
    sensor_state = models.IntegerField()
    sensor_sub = models.ForeignKey(EmbeddedSystem, related_name='belongs_to_subspace', on_delete=models.CASCADE)
    sensor_timerate = models.IntegerField()
    sensor_depth = models.IntegerField()
    sensor_type = models.ForeignKey(SensorType, related_name='has_type', on_delete=models.CASCADE)


class ReadType(models.Model):
    read_type_id = models.AutoField(primary_key=True)
    read_type_name = models.CharField(max_length=50)
    read_type_units = models.CharField(max_length=3)
    read_type_coef = models.IntegerField()
    read_type_sensor = models.ForeignKey(Sensor, related_name='read_belongs_to', on_delete=models.CASCADE)


class DayPlan(models.Model):
    dayplan_id = models.AutoField(primary_key=True)
    dayplan_gen_time = models.DateField(auto_now=True)
    dayplan_time = models.DateField()
    dayplan_water_qtd = models.IntegerField()
    dayplan_sub = models.ForeignKey(SubSpace, related_name='belongs_to_subspa', on_delete=models.CASCADE)


class Read(models.Model):
    read_id = models.AutoField(primary_key=True)
    read_timestamp = models.DateField(auto_now=True)
    read_value = models.IntegerField()
    read_sensor = models.ForeignKey(Sensor, related_name='belongs_to_sensor', on_delete=models.CASCADE)
    read_dayplan = models.ForeignKey(DayPlan, related_name='belongs_to_dayplan', on_delete=models.CASCADE)
    read_type = models.ForeignKey(ReadType, related_name='has_readtype', on_delete=models.CASCADE)


class Warnings(models.Model):
    warning_id = models.AutoField(primary_key=True)
    warning_description = models.CharField(max_length=300)


class IrrigationTime(models.Model):
    irrigation_time_id = models.AutoField(primary_key=True)
    irrigation_time_date = models.DateField()
    irrigation_time_qtd = models.IntegerField()
    irrigation_time_sub = models.ForeignKey(SubSpace, related_name='refers_to', on_delete=models.CASCADE)
