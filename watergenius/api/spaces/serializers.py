from rest_framework import serializers

from api.spaces.models import Space, TimeRestrition


class SpaceSerializer(serializers.ModelSerializer):
    space_id = serializers.PrimaryKeyRelatedField(queryset=Space.objects.all())
    class Meta:
        model = Space
        fields = ('space_id', 'space_name', 'space_description', 'space_irrigation_hour' ,'space_property','space_plant_type')
        validators = []  # Remove a default "unique together" constraint.

class TimeRestritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeRestrition
        fields = ('time_restrition_id','time_begin', 'time_duration', 'time_restrition_space')
        validators = []  # Remove a default "unique together" constraint.