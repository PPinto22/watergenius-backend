from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from api.models.sensors import Sensor
from api.serializers.sensors import SensorSerializer


class SensorsListView(APIView):
    def get(self, request):
        print(request.META['QUERY_STRING'])
        query = (request.META['QUERY_STRING']).split('=')
        if query[0] == 'embeddedsys':
            embeddedsys = (query[1])
            sensors = Sensor.objects.filter(sensor_sub_id=embeddedsys)
        else:
            if len(query) > 1:
                return Response('unknown query', HTTP_400_BAD_REQUEST)
            # nao sei se faz sentido seqer. devolver so as do user logaddo
            sensors = Sensor.objects.all()
        serialize = SensorSerializer(sensors, many=True)
        return Response(serialize.data, HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = SensorSerializer(data=data, partial=True)
        if serializer.is_valid():
            instance = serializer.create(serializer.validated_data)
            instance.save()
            return Response('OK', HTTP_200_OK)
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
        if serializer.is_valid():
            try:
                instance = Sensor.objects.get(sensor_id=sensid)
            except ObjectDoesNotExist as e:
                return Response('Especify the correct Sensor id', HTTP_400_BAD_REQUEST)
            for attr, value in serializer.validated_data.items():
                if attr != 'sensor_id':
                    setattr(instance, attr, value)
            instance.save()
            return Response('Sensor edited with success', HTTP_200_OK)
        else:
            return Response('Internal error or malformed json ', HTTP_400_BAD_REQUEST)

    def delete(self, request, sensid):
        try:
            sensors = Sensor.objects.get(sensor_id=sensid)
        except ObjectDoesNotExist as e:
            return Response("That  Sensor doesn't even exist, fool", HTTP_400_BAD_REQUEST)
        sensors.delete()
        return Response("Sensor deleted", HTTP_200_OK)