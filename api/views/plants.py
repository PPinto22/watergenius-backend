from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from api.models.plants import PlantType
from api.serializers.plants import PlantTypeSerializer


class PlantsListView(APIView):
    def get(self, request):
        plants = PlantType.objects.all()
        serializer = PlantTypeSerializer(plants, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class PlantDetailView(APIView):
    def get(self, request, plantid):
        plant = PlantType.objects.get(plant_type_id=plantid)
        return Response(PlantTypeSerializer(plant, many=False).data, HTTP_200_OK)
