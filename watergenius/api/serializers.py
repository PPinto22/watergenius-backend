from rest_framework import serializers

from api.models import *


class UserLoginSerializer(serializers.BaseSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=50)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name',  'last_name', 'is_superuser')
        validators = []  # Remove a default "unique together" constraint.

# TODO - validar email com regex
class UserCreateSerializer(serializers.ModelSerializer):
    is_superuser = serializers.BooleanField(required=False,default=False)
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'is_superuser')
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def create(self, validated_data):
        return User(**validated_data)

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('prop_id', 'prop_name', 'prop_description', 'prop_address' ,'prop_owner')
        validators = []  # Remove a default "unique together" constraint.

class SpaceSerializer(serializers.ModelSerializer):
    space_id = serializers.PrimaryKeyRelatedField(queryset=Space.objects.all())
    class Meta:
        model = Space
        fields = ('space_id', 'space_name', 'space_description', 'space_irrigation_hour' ,'space_property','space_plant_type')
        validators = []  # Remove a default "unique together" constraint.

class UserHasPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserHasProperty
        fields = ('user_has_id','prop_has_id')
        validators = []  # Remove a default "unique together" constraint.

class TimeRestritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeRestrition
        fields = ('time_restrition_id','time_begin', 'time_duration', 'time_restrition_space')
        validators = []  # Remove a default "unique together" constraint.

class PlantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantType
        fields = ('plant_type_id','plant_type_name')
        validators = []  # Remove a default "unique together" constraint.

class SubSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSpace
        fields = ('sub', 'sub_name', 'sub_description', 'sub_space_id')
        validators = []  # Remove a default "unique together" constraint.

class DayPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayPlan
        fields = ('dayplan_id', 'dayplan_gen_time', 'dayplan_time','dayplan_water_qtd', 'dayplan_sub')
        validators = []  # Remove a default "unique together" constraint.

class IrrigationTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IrrigationTime
        fields = ('irrigation_time_id', 'irrigation_time_date', 'irrigation_time_qtd', 'irrigation_time_sub')
        validators = []  # Remove a default "unique together" constraint.

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('sensor_id', 'sensor_state', 'sensor_sub', 'sensor_timerate' ,'sensor_depth','sensor_type')
        validators = []  # Remove a default "unique together" constraint.

class CentralNodeSerializer(serializers.ModelSerializer):
    node_id = serializers.PrimaryKeyRelatedField(queryset=CentralNode.objects.all())
    node_property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all())
    class Meta:
        model = CentralNode
        fields = ('node_id', 'node_ip', 'node_local', 'node_property' )
        validators = []  # Remove a default "unique together" constraint.

class ReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Read
        fields = ('read_id', 'read_timestamp', 'read_value', 'read_sensor' ,'read_dayplan','read_type')
        validators = []  # Remove a default "unique together" constraint.


class EmbeddedSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmbeddedSystem
        fields = ('esys_id', 'esys_local', 'esys_sub', 'esys_state')
        validators = []  # Remove a default "unique together" constraint.

class WarningsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warnings
        fields = ( 'warning_id', 'warning_description')
        validators = []  # Remove a default "unique together" constraint.



