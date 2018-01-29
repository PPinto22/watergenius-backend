from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *
# from time import gmtime, strftime
import datetime
from api.models.plans import DayPlan
from api.serializers.plans import DayPlanSerializer
from api.models.properties import UserManagesProperty, Property
from api.models.spaces import Space
from api.models.subspaces import SubSpace


def getPlansOfUser(user):
    if user.is_superuser:
        return DayPlan.objects.all()

    properties_managed = UserManagesProperty.objects.filter(user_id=user.email)
    spaces_managed = Space.objects.filter(space_property_id__in=properties_managed.values('prop_id'))
    subspaces_of_user = SubSpace.objects.filter(sub_space_id_id__in=spaces_managed.values('space_id'))
    dayplans = DayPlan.objects.filter(dayplan_sub__in=subspaces_of_user.values('sub_id'))
    return dayplans


class PlansListView(APIView):
    def get(self, request):
        dayplans = getPlansOfUser(request.user)
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
            dayplans = dayplans.filter(dayplan_sub_id__in=subspaces.values('sub_id'))
        except Exception as e:
            pass
        try:
            space_index = querylist.index('spaceid')
            spaceid = querylist[space_index + 1]
            space = Space.objects.get(space_id=spaceid)
            subspaces = SubSpace.objects.filter(sub_space_id_id=space.space_id)
            dayplans = dayplans.filter(dayplan_sub_id__in=subspaces.values('sub_id'))
        except Exception as e:
            pass
        try:
            subspace_index = querylist.index('subspaceid')
            subspaceid = querylist[subspace_index + 1]
            dayplans = dayplans.filter(dayplan_sub_id=subspaceid)
        except Exception as e:
            pass
        try:
            begin_date_index = querylist.index('begin_date')
            begin_date = querylist[begin_date_index + 1]
            dt = datetime.datetime.utcfromtimestamp(float(begin_date) / 1000)
            dayplans = dayplans.filter(dayplan_time__gte=dt)
        except Exception as e:
            pass
        try:
            end_date_index = querylist.index('end_date')
            end_date = querylist[end_date_index + 1]
            dt = datetime.datetime.utcfromtimestamp(float(end_date) / 1000)
            dayplans = dayplans.filter(dayplan_time__lte=dt)
        except Exception as e:
            pass

        # A order final é +dayplan_time. É revertida de seguida.
        dayplans = dayplans.order_by('-dayplan_time')

        # N planos mais recentes
        try:
            lastN = int(request.GET.get('last'))
            dayplans = dayplans[:lastN]
        except Exception as e:
            pass

        dayplans = reversed(dayplans)

        serialize = DayPlanSerializer(dayplans, many=True)
        return Response(serialize.data, HTTP_200_OK)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = DayPlanSerializer(data=data, partial=True)
        instance = DayPlan()
        if serializer.is_valid():
            for attr, value in serializer.validated_data.items():
                if attr != 'dayplan_id':
                    setattr(instance, attr, value)
            instance.save()
            serialize = DayPlanSerializer(instance, many=False)
            return Response(serialize.data, HTTP_200_OK)

        else:
            return Response('Internal error or malformed JSON ', HTTP_400_BAD_REQUEST)


class PlanDetailView(APIView):
    def get(self, request, planid):
        try:
            dayplans = DayPlan.objects.get(dayplan_id=planid)
        except ObjectDoesNotExist as e:
            return Response("That subspace doesn't even exist, fool", HTTP_400_BAD_REQUEST)
        serialize = DayPlanSerializer(dayplans, many=False)
        return Response(serialize.data, HTTP_200_OK)

    def delete(self, request, planid):
        try:
            dayplans = DayPlan.objects.get(dayplan_id=planid)
        except ObjectDoesNotExist as e:
            return Response("That subspace doesn't even exist, fool", HTTP_400_BAD_REQUEST)
        dayplans.delete()
        return Response("Dayplan deleted", HTTP_200_OK)

    def put(self, request, planid):
        data = JSONParser().parse(request)
        serializer = DayPlanSerializer(data=data, partial=True)
        if serializer.is_valid():
            try:
                instance = DayPlan.objects.get(dayplan_id=planid)
            except ObjectDoesNotExist as e:
                return Response('Specify the correct plan id', status=HTTP_400_BAD_REQUEST)
            for attr, value in serializer.validated_data.items():
                if attr != 'dayplan_id':
                    setattr(instance, attr, value)
            instance.save()
            serializer = DayPlanSerializer(instance, many=False)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response('Internal error or malformed json ', status=HTTP_400_BAD_REQUEST)
