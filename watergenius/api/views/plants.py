from django.http import JsonResponse

from api.models.plants import PlantType
from api.serializers.plants import PlantTypeSerializer


def plants(request):
    if request.method == 'GET':
        plants = PlantType.objects.all()
        serializer = PlantTypeSerializer(plants, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)

    return JsonResponse('error', status=400, safe=False)

# TODO - /plants/<id>
