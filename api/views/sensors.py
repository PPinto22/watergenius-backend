from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from api.models.embeddedsys import EmbeddedSystem
from api.models.properties import UserManagesProperty
from api.models.sensors import Sensor
from api.models.spaces import Space
from api.models.subspaces import SubSpace
from api.serializers.sensors import SensorSerializer


def getSensorsOfUser(user):
    if user.is_superuser:
        return Sensor.objects.all()
    
    properties_managed = UserManagesProperty.objects.filter(user_id=user.email)

    spaces = Space.objects.filter(space_property_id__in=properties_managed.values('prop'))
    subspaces = SubSpace.objects.filter(sub_space_id_id__in=spaces.values('space_id'))
    embeddedsys = EmbeddedSystem.objects.filter(esys_sub_id__in=subspaces.values('sub_id'))
    sensors = Sensor.objects.filter(sensor_esys_id__in=embeddedsys.values('esys_id'))
    return sensors

def getSensorsOfProperty(prop):
    spaces = Space.objects.filter(space_property_id=prop.prop_id)
    subspaces = SubSpace.objects.filter(sub_space_id_id__in=spaces.values('space_id'))
    embeddedsys = EmbeddedSystem.objects.filter(esys_sub_id__in=subspaces.values('sub_id'))
    sensors = Sensor.objects.filter(sensor_esys_id__in=embeddedsys.values('esys_id'))
    return sensors


class SensorsListView(APIView):
    def get(self, request):
        sensors = getSensorsOfUser(request.user)
        fullquery = (request.META['QUERY_STRING']).split('&')
        querylist = []
        for query in fullquery:
            querylist = querylist + (query.split('='))
        try:
            subspace_index = querylist.index('subspaceid')
            subspaceid = querylist[subspace_index + 1]
            embeddedsys = EmbeddedSystem.objects.filter(esys_sub_id=SubSpace.objects.get(sub_id=subspaceid))
            sensors = sensors.filter(sensor_esys_id__in=embeddedsys.values('esys_sub_id'))
        except Exception as e:
            print(e)
        try:
            embeddedsysid_index = querylist.index('embeddedsysid')
            embeddedsysid = querylist[embeddedsysid_index + 1]
            sensors = sensors.filter(sensor_esys_id=embeddedsysid)
        except Exception as e:
            print (e)
        serialize = SensorSerializer(sensors, many=True)
        return Response(serialize.data, HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = SensorSerializer(data=data, partial=True)
        if serializer.is_valid():
            instance = serializer.create(serializer.validated_data)
            instance.save()
            serialize = SensorSerializer(instance, many=False)
            return Response(serialize.data, HTTP_200_OK)
        else:
            return Response('Internal error or malformed JSON ', HTTP_400_BAD_REQUEST)


class SensorDetailView(APIView):
    def get(self, request, sensid):
        try:
            sensor = Sensor.objects.get(sensor_id=sensid)
        except ObjectDoesNotExist as e:
            return Response("That sensor  doesn't even exist, fool", HTTP_400_BAD_REQUEST)
        serialize = SensorSerializer(sensor, many=False)
        return Response(serialize.data, HTTP_200_OK)

    def put(self, request, sensid):
        data = JSONParser().parse(request)
        serializer = SensorSerializer(data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            try:
                instance = Sensor.objects.get(sensor_id=sensid)
            except ObjectDoesNotExist as e:
                return Response('Especify the correct Sensor id', HTTP_400_BAD_REQUEST)
            for attr, value in serializer.validated_data.items():
                if attr != 'sensor_id':
                    setattr(instance, attr, value)
            instance.save()
            serialize = SensorSerializer(instance, many=False)
            return Response(serialize.data, HTTP_200_OK)
        #else:
            #return Response('Internal error or malformed json ', HTTP_400_BAD_REQUEST)

    def delete(self, request, sensid):
        try:
            sensors = Sensor.objects.get(sensor_id=sensid)
        except ObjectDoesNotExist as e:
            return Response("That  Sensor doesn't even exist, fool", HTTP_400_BAD_REQUEST)
        sensors.delete()
        return Response("Sensor deleted", HTTP_200_OK)
