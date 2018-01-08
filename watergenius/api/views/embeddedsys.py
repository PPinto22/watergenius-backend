from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *

from api.models.embeddedsys import EmbeddedSystem
from api.serializers.embeddedsys import EmbeddedSystemSerializer


class EmbeddedSysListView(APIView):
    def get(self, request):
        embsystems = EmbeddedSystem.objects.all()
        fullquery = (request.META['QUERY_STRING']).split('&')
        querylist = []
        for query in fullquery :
            querylist = querylist + (query.split('='))
        try:
            subspace_index = querylist.index('subspace')
            subspaceid = querylist[subspace_index + 1]
            print(subspaceid)
            embsystems = embsystems.filter(esys_sub=subspaceid)
        except Exception as e:
            print (e)
            pass
        serialize = EmbeddedSystemSerializer(embsystems, many=True)
        return Response(serialize.data, HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = EmbeddedSystemSerializer(data=data, partial=True)
        if serializer.is_valid():
            instance = serializer.create(serializer.validated_data)
            instance.save()
            return Response('OK', HTTP_200_OK)
        else:
            return Response('Internal error or malformed JSON ', HTTP_400_BAD_REQUEST)

class EmbeddedSysDetailView(APIView):
    def get(self, request, sysid):
        try:
            esys = EmbeddedSystem.objects.get(esys_id=sysid)
        except ObjectDoesNotExist as e:
            return Response("That EmbeddedSystem  doesn't even exist, fool", HTTP_400_BAD_REQUEST)
        serialize = EmbeddedSystemSerializer(esys, many=False)
        return Response(serialize.data, HTTP_200_OK)

    def put(self, request, sysid):
        data = JSONParser().parse(request)
        serializer = EmbeddedSystemSerializer(data=data, partial=True)
        if serializer.is_valid():
            try:
                instance = EmbeddedSystem.objects.get(esys_id=sysid)
            except Exception as e:
                return Response('Especify the correct EmbeddedSystem id', HTTP_400_BAD_REQUEST)
            for attr, value in serializer.validated_data.items():
                if attr != 'esys_id':
                    setattr(instance, attr, value)
            instance.save()
            return Response('EmbeddedSystem edited with success', HTTP_200_OK)
        else:
            return Response('Internal error or malformed json ', HTTP_400_BAD_REQUEST)

    def delete(self, request, sysid):
        try:
            embsystems = EmbeddedSystem.objects.get(esys_id=sysid)
        except ObjectDoesNotExist as e:
            return Response("That  EmbeddedSystem doesn't even exist, fool", HTTP_400_BAD_REQUEST)
        embsystems.delete()
        return Response("EmbeddedSystem deleted", HTTP_204_NO_CONTENT)