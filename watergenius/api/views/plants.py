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