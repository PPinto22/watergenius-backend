from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from api.models.embeddedsys import EmbeddedSystem
from api.models.properties import UserManagesProperty
from api.models.reads import Read
from api.models.sensors import Sensor
from api.models.spaces import Space
from api.models.subspaces import SubSpace
from api.serializers.reads import ReadSerializer


def getReadsOfUser(user):
    if user.is_superuser:
        return Read.objects.all()

    properties_managed = UserManagesProperty.objects.filter(user_id=user.email)
    spaces_managed = Space.objects.filter(space_property_id__in=properties_managed.values('prop_id'))
    subspaces_of_user = SubSpace.objects.filter(sub_space_id_id__in=spaces_managed.values('space_id'))
    embeddedsys = EmbeddedSystem.objects.filter(esys_sub_id__in=subspaces_of_user)
    sensors = Sensor.objects.filter(sensor_esys_id__in=embeddedsys.values('esys_sub_id'))
    reads = Read.objects.filter(read_sensor_id__in=sensors.values('sensor_id'))
    return reads


class ReadsListView(APIView):
    def get(self, request):
        reads = getReadsOfUser(request.user)
        fullquery = (request.META['QUERY_STRING']).split('&')
        querylist = []
        for query in fullquery:
            querylist = querylist + (query.split('='))
        try:
            subspace_index = querylist.index('subspaceid')
            subspaceid = querylist[subspace_index + 1]
            embeddedsys = EmbeddedSystem.objects.filter(esys_sub_id=SubSpace.objects.get(sub_id=subspaceid).sub)
            sensors = Sensor.objects.filter(sensor_esys_id__in=embeddedsys.values('esys_sub_id'))
            reads = reads.filter(read_sensor_id__in=sensors.values('sensor_id'))
        except Exception as e:
            pass
        try:
            embeddedsysid_index = querylist.index('embeddedsysid')
            embeddedsysid = querylist[embeddedsysid_index + 1]
            sensors = Sensor.objects.filter(sensor_esys_id__in=embeddedsysid)
            reads = reads.filter(read_sensor_id__in=sensors.values('sensor_id'))
        except Exception as e:
            pass
        try:
            sensorid_index = querylist.index('sensorid')
            sensorid = querylist[sensorid_index + 1]
            sensors = Sensor.objects.get(sensor_id=sensorid)
            reads = reads.filter(read_sensor_id__in=sensors.sensor_id)
        except Exception as e:
            pass
        serialize = ReadSerializer(reads.order_by('read_timestamp'), many=True)
        return Response(serialize.data, HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = ReadSerializer(data=data, partial=True)
        if serializer.is_valid():
            instance = serializer.create(serializer.validated_data)
            instance.save()
            serialize = ReadSerializer(instance, many=False)
            return Response(serialize.data, HTTP_200_OK)
        else:
            return Response('Internal error or malformed JSON ', HTTP_400_BAD_REQUEST)


class ReadDetailView(APIView):
    def get(self, request, readid):
        try:
            read = Read.objects.get(read_id=readid)
        except ObjectDoesNotExist as e:
            return Response("That Read  doesn't even exist, fool", HTTP_400_BAD_REQUEST)
        serialize = ReadSerializer(read, many=False)
        return Response(serialize.data, HTTP_200_OK)

    def put(self, request, readid):
        if readid == None or readid == "":
            return Response('Especify the Read id in url', HTTP_400_BAD_REQUEST)
        data = JSONParser().parse(request)
        serializer = ReadSerializer(data=data, partial=True)
        if serializer.is_valid():
            try:
                instance = Read.objects.get(read_id=readid)
            except Exception as e:
                return Response('Especify the correct read id', HTTP_400_BAD_REQUEST)
            for attr, value in serializer.validated_data.items():
                if attr != 'read_id':
                    setattr(instance, attr, value)
            instance.save()
            serialize = ReadSerializer(instance, many=False)
            return Response(serialize.data, HTTP_200_OK)
        else:
            return Response('Internal error or malformed json ', HTTP_400_BAD_REQUEST)

    def delete(self, request, readid):
        # if readid!=None and readid!="":
        #    try:
        #        reads = Read.objects.get(read_id=readid)
        #    except ObjectDoesNotExist as e:
        #        return Response("That  Read doesn't even exist, fool" , HTTP_400_BAD_REQUEST)
        #    reads.delete()
        #    return Response( "Read deleted" , HTTP_200_OK)
        # else:
        # return Response(' Especify Read ID in url' , HTTP_400_BAD_REQUEST)
        return Response('Not Implemented', HTTP_400_BAD_REQUEST)
