from rest_framework import serializers

from api.models import SubSpace
from api.models.spaces import Space, TimeRestriction
from api.serializers.plants import PlantTypeSerializer
from api.serializers.subspaces import SubSpaceSerializer


class SpaceSerializer(serializers.ModelSerializer):
    space_id = serializers.PrimaryKeyRelatedField(queryset=Space.objects.all())

    def __init__(self, *args, nested_plant=False, nested_subspaces=False, **kwargs):
        super(SpaceSerializer, self).__init__(*args, **kwargs)

        if nested_plant:
            self.fields['space_plant_type'] = PlantTypeSerializer()
        if nested_subspaces:
            self.fields['space_subspaces'] = serializers.SerializerMethodField()

    def get_space_subspaces(self, space):
        subspaces = SubSpace.objects.filter(sub_space_id_id=space.space_id)
        return SubSpaceSerializer(instance=subspaces, many=True).data

    class Meta:
        model = Space
        fields = ('space_id', 'space_name', 'space_description',
                  'space_irrigation_hour', 'space_property', 'space_plant_type')
        validators = []  # Remove a default "unique together" constraint.


# class SpacePlantSerializer(serializers.ModelSerializer):
#
#     space_plant_type = PlantTypeSerializer()
#
#     class Meta:
#         model = Space
#         fields = ('space_id', 'space_name', 'space_description',
#                   'space_irrigation_hour', 'space_property', 'space_plant_type')


class TimeRestrictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeRestriction
        fields = ('time_restriction_id', 'time_restriction_begin', 'time_restriction_end', 'time_restriction_space')
        validators = []  # Remove a default "unique together" constraint.
