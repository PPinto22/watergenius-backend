from rest_framework import serializers

from api.models.subspaces import SubSpace


class SubSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSpace
        fields = ('sub_id', 'sub_name', 'sub_description', 'sub_space_id')
        validators = []  # Remove a default "unique together" constraint.
