from rest_framework import serializers
from api.models import User, Property , Space , PlantType, SubSpace

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

