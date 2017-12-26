from rest_framework import serializers

from api.properties.models import Property, CentralNode


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('prop_id', 'prop_name', 'prop_description', 'prop_address' ,'prop_owner')
        validators = []  # Remove a default "unique together" constraint.

class CentralNodeSerializer(serializers.ModelSerializer):
    node_id = serializers.PrimaryKeyRelatedField(queryset=CentralNode.objects.all())
    node_property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all())

    class Meta:
        model = CentralNode
        fields = ('node_id', 'node_ip', 'node_local', 'node_property')
        validators = []  # Remove a default "unique together" constraint.