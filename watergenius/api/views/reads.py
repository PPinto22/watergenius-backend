from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *

from api.models.reads import Read
from api.serializers.reads import ReadSerializer


class ReadsListView(APIView):
    def get(self, request):
        print(request.META['QUERY_STRING'])
        query = (request.META['QUERY_STRING']).split('=')
        if query[0] == 'sensor':
            sensor = (query[1])
            reads = Read.objects.filter(read_sensor_id=sensor)
        else:
            if len(query) > 1:
                return Response('unknown query', HTTP_400_BAD_REQUEST)
            # nao sei se faz sentido seqer. devolver so as do user logaddo
            reads = Read.objects.all()
        serialize = ReadSerializer(reads, many=True)
        return Response(serialize.data, HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = ReadSerializer(data=data, partial=True)
        if serializer.is_valid():
            instance = serializer.create(serializer.validated_data)
            instance.save()
            return Response('OK', HTTP_200_OK)
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
                if attr != 'sensor_id':
                    print(attr)
                    setattr(instance, attr, value)
            instance.save()
            return Response('Read edited with success', HTTP_200_OK)
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
