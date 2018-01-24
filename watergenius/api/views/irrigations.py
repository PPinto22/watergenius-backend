from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *
import datetime
from api.models.irrigations import IrrigationTime
from api.serializers.irrigations import IrrigationTimeSerializer
from api.models.properties import UserManagesProperty, Property
from api.models.spaces import Space
from api.models.subspaces import SubSpace


def getIrrigationsOfUser(user):
    if user.is_superuser:
        return IrrigationTime.objects.all()

    properties_managed = UserManagesProperty.objects.filter(user_id=user.email)
    spaces_managed = Space.objects.filter(space_property_id__in=properties_managed.values('prop_id'))
    subspaces_of_user = SubSpace.objects.filter(sub_space_id_id__in=spaces_managed.values('space_id'))
    irrigations = IrrigationTime.objects.filter(irrigation_time_sub__in=subspaces_of_user.values('sub_id'))
    return irrigations


class IrrigationTimeListView(APIView):
    def get(self, request):
        irrigations = getIrrigationsOfUser(request.user)
        fullquery = (request.META['QUERY_STRING']).split('&')
        querylist = []
        for query in fullquery:
            querylist = querylist + (query.split('='))
        try:
            property_index = querylist.index('propertyid')
            propertyid = querylist[property_index + 1]
            props = Property.objects.get(prop_id=propertyid)
            spaces = Space.objects.filter(space_property_id=props.prop_id)
            subspaces = SubSpace.objects.filter(sub_space_id_id__in=spaces.values('space_id'))
            irrigations = irrigations.filter(irrigation_time_sub__in=subspaces.values('sub_id'))
        except Exception as e:
            pass
        try:
            space_index = querylist.index('spaceid')
            spaceid = querylist[space_index + 1]
            space = Space.objects.get(space_id=spaceid)
            subspaces = SubSpace.objects.filter(sub_space_id_id=space.space_id)
            irrigations = irrigations.filter(irrigation_time_sub__in=subspaces.values('sub_id'))
        except Exception as e:
            pass

        try:
            subspace_index = querylist.index('subspaceid')
            subspaceid = querylist[subspace_index + 1]
            irrigations = irrigations.filter(irrigation_time_sub__in=subspaceid)
        except Exception as e:
            pass
        try:
            begin_date_index = querylist.index('begin_date')
            begin_date = querylist[begin_date_index + 1]
            dt = datetime.datetime.utcfromtimestamp(float(begin_date) / 1000)
            irrigations = irrigations.filter(irrigation_time_date__gte=dt)
        except Exception as e:
            pass
        try:
            end_date_index = querylist.index('end_date')
            end_date = querylist[end_date_index + 1]
            dt = datetime.datetime.utcfromtimestamp(float(end_date) / 1000)
            irrigations = irrigations.filter(irrigation_time_date__lte=dt)
        except Exception as e:
            pass
        serialize = IrrigationTimeSerializer(irrigations.order_by('irrigation_time_date'), many=True)
        return Response(serialize.data, HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = IrrigationTimeSerializer(data=data, partial=True)
        if serializer.is_valid():
            instance = serializer.create(serializer.validated_data)
            instance.save()
            serialize = IrrigationTimeSerializer(instance, many=False)
            return Response(serialize.data, HTTP_200_OK)
        else:
            return Response('Internal error or malformed JSON ', HTTP_400_BAD_REQUEST)


class IrrigationTimeDetailView(APIView):
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
                return Response('Especify the correct restriction id', HTTP_400_BAD_REQUEST)
            for attr, value in serializer.validated_data.items():
                if attr != 'irrigation_time_id':
                    setattr(instance, attr, value)
            instance.save()
            serialize = IrrigationTimeSerializer(instance, many=False)
            return Response(serialize.data, HTTP_200_OK)
        else:
            return Response('Internal error or malformed json ', HTTP_400_BAD_REQUEST)

    def delete(self, request, irrigationid):
        try:
            dayplans = IrrigationTime.objects.get(irrigation_time_id=irrigationid)
        except ObjectDoesNotExist as e:
            return Response("That Irrigation time doesn't even exist, fool", HTTP_400_BAD_REQUEST)
        dayplans.delete()
        return Response("IrrigationTime deleted", HTTP_200_OK)
