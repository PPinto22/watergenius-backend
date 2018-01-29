from rest_framework import serializers

from api.models import SubSpace
from api.models.spaces import Space, TimeRestriction
from api.serializers.plants import PlantTypeSerializer
from api.serializers.subspaces import SubSpaceSerializer


class SpaceSerializer(serializers.ModelSerializer):
    space_id = serializers.PrimaryKeyRelatedField(queryset=Space.objects.all())

    def __init__(self, *args, nested_plant=False, nest_level='spaces', **kwargs):
        super(SpaceSerializer, self).__init__(*args, **kwargs)

        self.nest_level = nest_level

        if nested_plant:
            self.fields['space_plant_type'] = PlantTypeSerializer()
        if nest_level in ['subspaces', 'embeddedsys', 'sensors']:
            self.fields['space_subspaces'] = serializers.SerializerMethodField()

    def get_space_subspaces(self, space):
        subspaces = SubSpace.objects.filter(sub_space_id_id=space.space_id)
        return SubSpaceSerializer(instance=subspaces, nest_level=self.nest_level, many=True).data

    class Meta:
        model = Space
        fields = ('space_id', 'space_name', 'space_description',
                  'space_irrigation_hour', 'space_property', 'space_plant_type')
        validators = []  # Remove a default "unique together" constraint.


class TimeRestrictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeRestriction
        fields = ('time_restriction_id', 'time_restriction_begin', 'time_restriction_end', 'time_restriction_space')
        validators = []  # Remove a default "unique together" constraint.
