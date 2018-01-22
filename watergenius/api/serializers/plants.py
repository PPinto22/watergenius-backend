from rest_framework import serializers

from api.models.plants import PlantType


class PlantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantType
        fields = ('plant_type_id', 'plant_type_name_eng', 'plant_type_name_por')
        validators = []  # Remove a default "unique together" constraint.
