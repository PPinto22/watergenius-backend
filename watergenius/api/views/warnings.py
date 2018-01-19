from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *

from api.models.warnings import Warning
from api.serializers.warnings import WarningSerializer
from api.models.properties import Property, UserManagesProperty


class WarningsListView(APIView):
    def get(self, request):
        properties_managed = UserManagesProperty.objects.filter(user_id=request.user.email)
        warnings = Warning.objects.filter(warning_property__in=properties_managed.values('prop_id'))
        fullquery = (request.META['QUERY_STRING']).split('&')
        querylist = []
        for query in fullquery:
            querylist = querylist + (query.split('='))
        try:
            property_index = querylist.index('propertyid')
            propertyid = querylist[property_index + 1]
            warnings = warnings.filter(warning_property=propertyid)
        except Exception as e:
            print(e)
            pass
        serialize = WarningSerializer(warnings, many=True)
        return Response(serialize.data, HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = WarningSerializer(data=data, partial=True)
        if serializer.is_valid():
            instance = serializer.create(serializer.validated_data)
            instance.save()
            serialize = WarningSerializer(instance, many=False)
            return Response(serialize.data, HTTP_200_OK)
        else:
            return Response('Internal error or malformed JSON ', HTTP_400_BAD_REQUEST)
