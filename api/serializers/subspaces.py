from rest_framework import serializers

from api.models import EmbeddedSystem, SubSpace
from api.serializers.embeddedsys import EmbeddedSystemSerializer


class SubSpaceSerializer(serializers.ModelSerializer):

    def __init__(self, *args, nest_level='subspace', **kwargs):
        super(SubSpaceSerializer, self).__init__(*args, **kwargs)

        self.nest_level = nest_level

        if nest_level in ['embeddedsys', 'sensors']:
            self.fields['sub_embeddedsys'] = serializers.SerializerMethodField()

    def get_sub_embeddedsys(self, subspace):
        esys = EmbeddedSystem.objects.filter(esys_sub=subspace.sub_id)
        return EmbeddedSystemSerializer(instance=esys, nest_level=self.nest_level, many=True).data

    class Meta:
        model = SubSpace
        fields = ('sub_id', 'sub_name', 'sub_description', 'sub_space_id')
        validators = []  # Remove a default "unique together" constraint.
