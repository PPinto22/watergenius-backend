from django.http import JsonResponse
from rest_framework.parsers import JSONParser

from api.models.warnings import Warning
from api.serializers.warnings import WarningSerializer


def warnings(request):
    if request.method == 'GET':
        #query = (request.META['QUERY_STRING']).split('=')
        #if query[0] == 'centralnode':
        #    centralnode = (query[1])
        #    dayplans = Read.objects.filter(warning_central=centralnode)
        #else:
        #    if len(query)>1:
        #        return JsonResponse('unknown query', status=400, safe=False)
            #nao sei se faz sentido seqer. devolver so as do user logaddo
        warnings = Warning.objects.all()
        serialize = WarningSerializer(warnings, many=True)
        return JsonResponse( serialize.data , status=200 ,safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = WarningSerializer(data=data , partial=True)
        instance = Warning()
        if serializer.is_valid():
            for attr, value in serializer.validated_data.items():
                if attr != 'warning_id' :
                    setattr(instance, attr, value)
            instance.save()
            return  JsonResponse( 'OK', status=200, safe=False)
        else:
             return JsonResponse('Internal error or malformed JSON ' , status=500 ,safe=False)
    return JsonResponse('error', status=400, safe=False)

