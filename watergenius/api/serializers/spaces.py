from rest_framework import serializers

from api.models.spaces import Space, TimeRestriction


class SpaceSerializer(serializers.ModelSerializer):
    space_id = serializers.PrimaryKeyRelatedField(queryset=Space.objects.all())

    class Meta:
        model = Space
        fields = (
        'space_id', 'space_name', 'space_description', 'space_irrigation_hour', 'space_property', 'space_plant_type')
        validators = []  # Remove a default "unique together" constraint.


class TimeRestrictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeRestriction
        fields = ('time_restriction_id', 'time_restriction_begin', 'time_restriction_end', 'time_restriction_space')
        validators = []  # Remove a default "unique together" constraint.
