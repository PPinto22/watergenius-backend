from rest_framework import serializers
from api.models import User, Property , Warnings,  Space , EmbeddedSystem,  Read,  PlantType, SubSpace , DayPlan , IrrigationTime , Sensor

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_email', 'user_name', 'user_admin')
        validators = []  # Remove a default "unique together" constraint.

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('prop_id', 'prop_name', 'prop_description', 'prop_address' ,'prop_owner')
        validators = []  # Remove a default "unique together" constraint.

class SpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = ('space_id', 'space_name', 'space_description', 'space_irrigation_hour' ,'space_property','space_plant_type')
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



