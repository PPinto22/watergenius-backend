from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from api.models import Space
from api.models.properties import Property, CentralNode, UserManagesProperty
from api.serializers.spaces import SpaceSerializer


class PropertySerializer(serializers.ModelSerializer):
    def __init__(self, *args, nested_node=False, nested_spaces=False, nested_subspaces=False, **kwargs):
        super(PropertySerializer, self).__init__(*args, **kwargs)

        self.nested_node = nested_node
        self.nested_spaces = nested_spaces
        self.nested_subspaces = nested_subspaces

        if nested_node:
            self.fields['prop_node'] = serializers.SerializerMethodField()
        if nested_spaces or nested_subspaces:
            self.fields['prop_spaces'] = serializers.SerializerMethodField()

    def get_prop_node(self, prop):
        try:
            node = CentralNode.objects.get(node_property=prop.prop_id)
            return CentralNodeSerializer(instance=node).data
        except ObjectDoesNotExist:
            return {}  # Empty

    def get_prop_spaces(self, prop):
        spaces = Space.objects.filter(space_property_id=prop.prop_id)
        return SpaceSerializer(instance=spaces, nested_subspaces=self.nested_subspaces, many=True).data

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
