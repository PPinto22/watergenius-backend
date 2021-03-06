from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *

from api.models.embeddedsys import EmbeddedSystem
from api.serializers.embeddedsys import EmbeddedSystemSerializer
from api.views.subspaces import getSubspacesByUser


def getEmbeddedSystemsOfUser(user):
    embeddedSys = EmbeddedSystem.objects.all()
    if user.is_superuser:
        return embeddedSys

    subspaces = getSubspacesByUser(user)
    return embeddedSys.filter(esys_sub__in=subspaces.values('sub_id'))


class EmbeddedSysListView(APIView):
    def get(self, request):
        embsystems = getEmbeddedSystemsOfUser(request.user)
        fullquery = (request.META['QUERY_STRING']).split('&')
        querylist = []
        for query in fullquery:
            querylist = querylist + (query.split('='))
        try:
            subspace_index = querylist.index('subspaceid')
            subspaceid = querylist[subspace_index + 1]
            embsystems = embsystems.filter(esys_sub=subspaceid)
        except Exception as e:
            pass
        serialize = EmbeddedSystemSerializer(embsystems,
                                             nest_level=request.GET.get('nest_level', 'embeddedsys'),
                                             many=True)
        return Response(serialize.data, HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = EmbeddedSystemSerializer(data=data, partial=True)
        if serializer.is_valid():
            instance = serializer.create(serializer.validated_data)
            instance.save()
            serialize = EmbeddedSystemSerializer(instance, many=False)
            return Response(serialize.data, HTTP_200_OK)
        else:
            return Response('Internal error or malformed JSON ', HTTP_400_BAD_REQUEST)


class EmbeddedSysDetailView(APIView):
    def get(self, request, sysid):
        try:
            esys = EmbeddedSystem.objects.get(esys_id=sysid)
        except ObjectDoesNotExist as e:
            return Response("That EmbeddedSystem  doesn't even exist, fool", HTTP_400_BAD_REQUEST)
        serialize = EmbeddedSystemSerializer(esys,
                                             nest_level=request.GET.get('nest_level', 'embeddedsys'),
                                             many=False)
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
            serialize = EmbeddedSystemSerializer(instance, many=False)
            return Response(serialize.data, HTTP_200_OK)
        else:
            return Response('Internal error or malformed json ', HTTP_400_BAD_REQUEST)

    def delete(self, request, sysid):
        try:
            embsystems = EmbeddedSystem.objects.get(esys_id=sysid)
        except ObjectDoesNotExist as e:
            return Response("That  EmbeddedSystem doesn't even exist, fool", HTTP_400_BAD_REQUEST)
        embsystems.delete()
        return Response("EmbeddedSystem deleted", HTTP_200_OK)
