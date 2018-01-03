from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *

from api.models.irrigations import IrrigationTime
from api.serializers.irrigations import IrrigationTimeSerializer


class IrrigationsListView(APIView):
    def get(self, request):
        print(request.META['QUERY_STRING'])
        query = (request.META['QUERY_STRING']).split('=')
        if query[0] == 'subspace':
            print('é isso evaristo')
            subspaceid = (query[1])
            irrigations = IrrigationTime.objects.filter(irrigation_time_sub=subspaceid)
        else:
            if len(query) > 1:
                return Response('unknown query', HTTP_400_BAD_REQUEST)
            # nao sei se faz sentido seqer. devolver so as do user logaddo
            # irrigations = Irrigation.objects.filter()
            irrigations = IrrigationTime.objects.all()
        serialize = IrrigationTimeSerializer(irrigations, many=True)
        return Response(serialize.data, HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = IrrigationTimeSerializer(data=data, partial=True)
        if serializer.is_valid():
            instance = serializer.create(serializer.validated_data)
            instance.save()
            return Response('OK', HTTP_200_OK)
        else:
            return Response('Internal error or malformed JSON ', HTTP_400_BAD_REQUEST)

class IrrigationDetailView(APIView):
    def get(self, request, irrigationid):
        try:
            irrigation = IrrigationTime.objects.get(irrigation_time_id=irrigationid)
        except ObjectDoesNotExist as e:
            return Response("That irrigation action doesn't even exist, fool", HTTP_400_BAD_REQUEST)
        serialize = IrrigationTimeSerializer(irrigation, many=False)
        return Response(serialize.data, HTTP_200_OK)

    def put(self, request, irrigationid):
        data = JSONParser().parse(request)
        serializer = IrrigationTimeSerializer(data=data, partial=True)
        if serializer.is_valid():
            try:
                instance = IrrigationTime.objects.get(irrigation_time_id=irrigationid)
            except Exception as e:
                return Response('Especify the correct restrition id', HTTP_400_BAD_REQUEST)
            for attr, value in serializer.validated_data.items():
                if attr != 'irrigation_time_id':
                    print(attr)
                    setattr(instance, attr, value)
            instance.save()
            return Response('IrrigationTime edited with success', HTTP_200_OK)
        else:
            return Response('Internal error or malformed json ', HTTP_400_BAD_REQUEST)

    def delete(self, request, irrigationid):
        try:
            dayplans = IrrigationTime.objects.get(irrigation_time_id=irrigationid)
        except ObjectDoesNotExist as e:
            return Response("That Irrigation time doesn't even exist, fool", HTTP_400_BAD_REQUEST)
        dayplans.delete()
        return Response("IrrigationTime deleted", HTTP_204_NO_CONTENT)
