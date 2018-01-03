from rest_framework import serializers

from api.models.embeddedsys import EmbeddedSystem



#class LocalizationSerializer(serializers.ModelSerializer):
    
#    class Meta:
#        model = Localization
#        fields = ('local_id', 'local_lat' , 'local_long' )
#        validators = []  # Remove a default "unique together" constraint.

class EmbeddedSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmbeddedSystem
        fields = ('esys_id', 'esys_local_long',  'esys_local_lat',  'esys_local_alt', 'esys_sub', 'esys_state', 'esys_name' , 'esys_network_pass')
        validators = []  # Remove a default "unique together" constraint.
	