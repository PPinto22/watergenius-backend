from rest_framework import serializers

from api.models import User, Property, Space, PlantType, SubSpace, DayPlan


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
