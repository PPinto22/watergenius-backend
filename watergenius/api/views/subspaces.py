from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from api.models.subspaces import SubSpace
from api.serializers.subspaces import SubSpaceSerializer


class SubspacesListView(APIView):
    def get(self, request):
        plants = SubSpace.objects.all()
        serialize = SubSpaceSerializer(plants, many=True)
        return Response(serialize.data, HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = SubSpaceSerializer(data=data, partial=True)
        if serializer.is_valid():
            instance = serializer.create(serializer.validated_data)
            instance.save()
            return Response('OK', HTTP_200_OK)
        else:
            return Response('Internal error or malformed JSON ', HTTP_400_BAD_REQUEST)

class SubspaceDetailView(APIView):
    def get(self, request, subspaceid):
        plants = SubSpace.objects.filter(sub=subspaceid)
        serialize = SubSpaceSerializer(plants, many=True)
        return Response(serialize.data, HTTP_200_OK)

    def put(self, request, subspaceid):
        data = JSONParser().parse(request)
        serializer = SubSpaceSerializer(data=data, partial=True)
        if serializer.is_valid():
            try:
                instance = SubSpace.objects.get(sub=subspaceid)
            except Exception as e:
                return Response('Especify the correct restrition id', HTTP_400_BAD_REQUEST)
            for attr, value in serializer.validated_data.items():
                if attr != 'sub':
                    print(attr)
                    setattr(instance, attr, value)
            instance.save()
            return Response('Subsapce edited with success', HTTP_200_OK)
        else:
            return Response('Internal error or malformed json ', HTTP_400_BAD_REQUEST)

    def delete(self, request, subspaceid):
        try:
            space = SubSpace.objects.get(sub=subspaceid)
        except ObjectDoesNotExist:
            return Response("That subspace doesn't even exist, fool", HTTP_400_BAD_REQUEST)
        space.delete()
        return Response('SubSpace deleted', HTTP_204_NO_CONTENT)
