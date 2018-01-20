from rest_framework import serializers

from api.models.properties import Property, CentralNode, UserManagesProperty


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('prop_id', 'prop_name', 'prop_description', 'prop_address', 'prop_owner')
        validators = []  # Remove a default "unique together" constraint.


class CentralNodeSerializer(serializers.ModelSerializer):
    node_property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all())

    class Meta:
        model = CentralNode
        fields = ('node_ip', 'node_local_lat', 'node_local_long', 'node_local_alt', 'node_property',
                  'node_network_name', 'node_network_password')
        validators = []  # Remove a default "unique together" constraint.


class UserManagesPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserManagesProperty
        fields = ('user_id', 'prop_id')
        validators = []  # Remove a default "unique together" constraint.
