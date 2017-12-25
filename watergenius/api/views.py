from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist 
import api.serializers
from api.serializers import *


class RegisterView(APIView):
    # TODO - Registar admin: verificar se is_admin = True
    permission_classes = [AllowAny]
    def post(self, request):
        data = JSONParser().parse(request)
        user_ser = UserCreateSerializer(data=data)
        # Email unico validado aqui
        user_ser.is_valid(raise_exception=True)
        user = user_ser.create(user_ser.validated_data)
        user.set_password(user.password)
        user.save()
        return Response(UserSerializer(user).data)


class UserView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = api.serializers.UserSerializer(users, many=True)
        return Response(serializer.data)


# TODO - Testar se tudo daqui para baixo ainda funciona depois de eu ter andado a mexer na autenticacao.
# TODO - Passar para class views ?
def usersMail(request, mail=None):
    if request.method == 'GET':
        #data = JSONParser().parse(request)
        user = User.objects.get(user_email=mail)
        serializer = api.serializers.UserSerializer(user, many=False)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        #editar user
        user = User.objects.get(user_email=mail)
        data = JSONParser().parse(request)
        serializer = api.serializers.UserSerializer(data=data, partial=True)
        print(serializer.is_valid())
        # assuming that serializer is valid. TODO 
        if serializer.data['user_email']==user.email:
            user.name = serializer.data['user_name']
            user.admin = serializer.data['user_admin']
            user.save()
            return JsonResponse(serializer.data, status=201)
    elif request.method == 'DELETE':
        user = User.objects.get(user_email=mail)
        print(user)
        if user:
            user.delete()
            return JsonResponse( 'OK', status=200, safe=False)


    return JsonResponse(serializer.errors, status=400)


#/properties/{id}/managers
def propertiesManagers(request, propid=None, managerid=None):
    print(managerid)
    print(propid)
    if propid==None:
        return JsonResponse(' Please especify the property id' , status=400 ,safe=False)
    if request.method == 'GET':
        if managerid==None:
            #return all managers of that property
            managersOfProperty = UserHasProperty.objects.filter(prop_has_id=propid)
            queryset = User.objects.filter(email__in=managersOfProperty.values('user_has_id'))
            print(list(queryset))
            serializer = api.serializers.UserSerializer(list(queryset), many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            managersOfProperty = UserHasProperty.objects.filter(prop_has_id=propid)
            queryset = User.objects.filter(email__in=managersOfProperty.values('user_has_id'), )

    if request.method == 'PUT':
        if managerid!=None:
            #NOTE: put = set user has manager??
            try:
                user = User.objects.get(email=managerid)
            except Exception as e:
                return JsonResponse(' Invalid user mail ' , status=400 ,safe=False)
            manager = UserHasProperty()
            manager.user_has_id = user
            manager.prop_has_id =  Property.objects.get(prop_id=propid)
            try:
                manager.save()
            except Exception:
                return JsonResponse( managerid + ' is the manager already' , status=200 ,safe=False)
            return JsonResponse('New Manager added' , status=200 ,safe=False)
        else:
            return JsonResponse(' Please especify the property id' , status=400 ,safe=False)

    if request.method == 'DELETE':
        if managerid!=None:
            try:
                usp = UserHasProperty.objects.get(user_has_id=managerid , prop_has_id=propid)
            except ObjectDoesNotExist:
                return JsonResponse("That manager doesn't manage this property" , status=400 ,safe=False)
            usp.delete()
            return JsonResponse('OK', status=200, safe=False)
        else:
            return JsonResponse('Especify the property id' , status=400 ,safe=False)


    return JsonResponse('Not supported' + str(propid) + str(), status=400, safe=False)



#/properties/{id}/node
def propertiesNode(request, propid=None):
    if propid==None:
        return JsonResponse(' Please especify the property id' , status=400 ,safe=False)
    
    if request.method == 'GET':
        try:
            node = CentralNode.objects.get(node_property_id=propid)
        except ObjectDoesNotExist as e:
            return JsonResponse("That property doesn't have a central node" , status=404, safe=False)
        
        serializer = CentralNodeSerializer(node, many=False)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        try:
            node = CentralNode.objects.get(node_property_id=propid)
        except ObjectDoesNotExist as e:
            data = JSONParser().parse(request)
            serializer = api.serializers.CentralNodeSerializer(data=data , partial=True)
            if serializer.is_valid():
                serializer.node_id=-1
                serializer.save()
                return JsonResponse('Central Node created' , status=200 ,safe=False)
        else:
            # already exists, error
             return JsonResponse('That property already has a central node. if you want to edit the central node, use post method' , status=200 ,safe=False)
    elif request.method == 'POST':
        try:
            node = CentralNode.objects.get(node_property_id=propid)
        except ObjectDoesNotExist as e:
            return JsonResponse("That property doesn't have a central node" , status=404, safe=False)
        data = JSONParser().parse(request)
        serializer = api.serializers.CentralNodeSerializer(data=data , partial=True)
        print(serializer.is_valid())
        print(serializer.data)
        if serializer.is_valid():
            for attr, value in serializer.validated_data.items():
                # NOTE: not allowing to change property id . DISCUSS
                if attr != 'node_id' and attr != 'node_property':
                    setattr(node, attr, value)
            node.save()
            return JsonResponse('Central Node updated' , status=200 ,safe=False)
        else:
            return JsonResponse('Internal error' , status=500 ,safe=False)                    
    return JsonResponse('NOT SUPPORTED' + str(propid), status=400, safe=False)


#Propertys/{id}
def properties(request, propid=None):
    if request.method == 'GET':
        #data = JSONParser().parse(request)
        if propid!=None:
            #TODO  check authenticated user and get only the properties of that user
            prop = Property.objects.filter(prop_id=propid)
            print (prop)
            serializer = api.serializers.PropertySerializer(list(prop) , many=True)
            return JsonResponse(serializer.data , status=200 ,safe=False)
        else:
            owner = request.user
            print(owner)
            prop = Property.objects.filter(prop_owner_id=owner)
            serializer = api.serializers.PropertySerializer(prop, many=True)
            return JsonResponse(serializer.data , status=200 ,safe=False)
    
    elif request.method == 'POST':
        print('ao poste')
        if propid!=None:
            try:
                instance = Property.objects.get(prop_id=propid)
            except ObjectDoesNotExist:
                return JsonResponse("That property doesn't even exist" , status=400 ,safe=False)
            data = JSONParser().parse(request)
            serializer = api.serializers.PropertySerializer(data=data , partial=True)
            if serializer.is_valid():
                for attr, value in serializer.validated_data.items():
                    print (attr)
                    if attr != 'prop_id' and attr != 'prop_owner':
                        setattr(instance, attr, value)
                print(type(instance))
                instance.save()
                return JsonResponse('Property updated' , status=200 ,safe=False)
        else:
            return JsonResponse('Especify the property id' , status=400 ,safe=False)
    elif request.method == 'PUT':
        # NOTE : not inserting in api_userhasproperty DISCUSS
        if propid!=None:
            #especificou id no url ( makes sense? dunno)
            try:
                instance = Property.objects.get(prop_id=propid)
            except ObjectDoesNotExist:
                instance = None
            if instance != None:
                data = JSONParser().parse(request)
                serializer = api.serializers.PropertySerializer(data=data , partial=True)
                if serializer.is_valid():
                    if serializer.is_valid():
                        for attr, value in serializer.validated_data.items():
                            print (attr)
                            if attr != 'prop_id' or attr != 'prop_owner':
                                setattr(instance, attr, value)
                        instance.save()
                    return JsonResponse('Property updated' , status=200 ,safe=False)
                else:
                    return JsonResponse('Internal error' , status=500 ,safe=False)                    
            else:
                #doesn't exist, create
                data = JSONParser().parse(request)
                serializer = api.serializers.PropertySerializer(data=data , partial=True)
                if serializer.is_valid():
                    serializer.prop_id=-1
                    serializer.save()
                    return JsonResponse('New property created' , status=200 ,safe=False)

        else:
            #create the resource with auto id
            data = JSONParser().parse(request)
            serializer = api.serializers.PropertySerializer(data=data , partial=True)
            if serializer.is_valid():
                serializer.prop_id=-1
                serializer.save()
                return JsonResponse('New property created' , status=200 ,safe=False)
            else:
                return JsonResponse('Internal error' , status=500 ,safe=False)                    
    
    elif request.method == 'DELETE':
        if propid!=None:
            try:
                prop = Property.objects.get(prop_id=propid)
            except ObjectDoesNotExist:
                return JsonResponse("That property doesn't even exist" , status=400 ,safe=False)
            prop.delete()
            return JsonResponse('OK', status=200, safe=False)
        else:
            return JsonResponse('Especify the property id' , status=400 ,safe=False)

    return JsonResponse('error', status=501, safe=False)



def spaces(request, spaceid=None):
    if request.method == 'GET':
        print(spaceid)
        if spaceid!=None:
            #TODO get this user email with the pinto way
            props = Property.objects.filter(prop_owner_id=request.user.email)
            queryset = Space.objects.filter(space_property__in=props.values('prop_id'))
            print(list(queryset))
            spaces = api.serializers.SpaceSerializer(list(queryset), many=True)
            return JsonResponse( spaces.data, status=200 ,safe=False)
        else:
            queryset = Space.objects.all()
            spaces = api.serializers.SpaceSerializer(queryset, many=True)
            return JsonResponse( spaces.data, status=200 ,safe=False)

    elif request.method == 'POST':
        #edit resource
        data = JSONParser().parse(request)
        serializer = api.serializers.SpaceSerializer(data=data , partial=True)
        if serializer.is_valid():
            instance = Space.objects.get(pk=serializer.data['space_id'])
            print(instance)
            for attr, value in serializer.validated_data.items():
                print (attr)
                if attr != 'space_id':
                    setattr(instance, attr, value)
            print(type(instance))
            instance.save()
            return JsonResponse( 'OK', status=200, safe=False)

    elif request.method == 'PUT':
        print('put')
        if spaceid!=None:
            try:
                space = Space.objects.get(space_id=spaceid)
            except ObjectDoesNotExist as e:
                #insert
                print('nao existe')
                instance = Space()
                data = JSONParser().parse(request)
                serializer = api.serializers.SpaceSerializer(data=data , partial=True)
                if serializer.is_valid():
                    for attr, value in serializer.validated_data.items():
                        if attr != 'space_id' :
                            print (attr)
                            setattr(instance, attr, value)
                    try:
                        space1 = Space.objects.get(space_id=serializer.data['space_id'])
                    except ObjectDoesNotExist as e:
                        instance.save()
                        return  JsonResponse( 'OK', status=200, safe=False)
                    else:
                        return JsonResponse('a space with that id already exists. if you want to edit it, use post method' , status=200 ,safe=False)
                return JsonResponse('Internal error' , status=500 ,safe=False)                                       
            else:
                #already exists , overwrite or ignore?? DISCUSS
                return JsonResponse('This space in url already exists. if you want to edit it, use post method' , status=200 ,safe=False)

        else:
            instance = Space()
            data = JSONParser().parse(request)
            serializer = api.serializers.SpaceSerializer(data=data , partial=True)
            if serializer.is_valid():
                for attr, value in serializer.validated_data.items():
                    if attr != 'space_id' :
                        print (attr)
                        setattr(instance, attr, value)
                instance.save()
                return  JsonResponse( 'OK', status=200, safe=False)
                
            return JsonResponse('Internal error' , status=500 ,safe=False)
    elif request.method == 'DELETE':
        if spaceid!=None:
            try:
                space = Space.objects.get(space_id=spaceid)
            except ObjectDoesNotExist:
                return JsonResponse("That space doesn't even exist, fool" , status=400 ,safe=False)
            space.delete()
            return JsonResponse('Space deleted', status=200, safe=False)
        else:
            return JsonResponse(' Especify space ID in url' , status=400 ,safe=False)

    return JsonResponse('error', status=400, safe=False)

#def spaceResSimple()

#spaces/id/restritions/id
def spacesRes(request, spaceid, resid=None):
    if request.method == 'GET':
        if resid ==None or resid =="":
            if spaceid==None:
                return JsonResponse(' Especify space ID in url' , status=400 ,safe=False)
            timeRes = TimeRestrition.objects.filter(time_restrition_space=spaceid)
            serializer = api.serializers.TimeRestritionSerializer(list(timeRes), many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
        else:
            #resid is valid
            try:
                timeRes = TimeRestrition.objects.get(time_restrition_id=resid)
            except ObjectDoesNotExist as e:
                return JsonResponse(' the especified time restrition doesnt exist for that space' , status=400 ,safe=False)
            
            serializer = api.serializers.TimeRestritionSerializer(timeRes, many=False)
            return JsonResponse(serializer.data, status=200, safe=False)

    elif request.method == 'PUT':
        instance = TimeRestrition()
        data = JSONParser().parse(request)
        serializer = api.serializers.TimeRestritionSerializer(data=data , partial=True)
        if serializer.is_valid():
            for attr, value in serializer.validated_data.items():
                if attr != 'time_restrition_id' :
                    print (attr)
                    setattr(instance, attr, value)
            instance.save()
            return  JsonResponse( 'OK', status=200, safe=False)
        else:
            return JsonResponse('Internal error or malformed json ' , status=500 ,safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = api.serializers.TimeRestritionSerializer(data=data , partial=True)
        if serializer.is_valid():
            if resid ==None or resid =="":
                resid = serializer.validated_data['time_restrition_id']
            try:
                instance = TimeRestrition.objects.get(time_restrition_id=resid)
            except Exception as e:
                return JsonResponse('Especify the correct restrition id' , status=400 ,safe=False)
            for attr, value in serializer.validated_data.items():
                if attr != 'time_restrition_id' :
                    print (attr)
                    setattr(instance, attr, value)
            instance.save()
            return JsonResponse( 'Time restrition edited with success', status=200, safe=False)
        else:
            return JsonResponse('Internal error or malformed json ' , status=500 ,safe=False)

    elif request.method == 'DELETE':
        if resid!=None and resid !="":
            try:
                time = TimeRestrition.objects.filter(time_restrition_id=resid, time_restrition_space=spaceid)
            except ObjectDoesNotExist:
                return JsonResponse("That restrition doesn't even exist, fool" , status=400 ,safe=False)
            if len(time) >0:
                time.delete()
                return JsonResponse('restrition deleted', status=200, safe=False)

            return JsonResponse("That restrition doesn't even exist for that space, fool" , status=400 ,safe=False)
        else:
            return JsonResponse(' Especify space ID in url' , status=400 ,safe=False)

    return JsonResponse('error' + str(spaceid)+ str(resid), status=400, safe=False)


def plants(request):
    if request.method == 'GET':
        plants = PlantType.objects.all()
        serializer = api.serializers.PlantTypeSerializer(plants, many=True)
        return JsonResponse( serializer.data, status=200 ,safe=False)
    elif request.method == 'PUT':
        print ('iii')

    return JsonResponse('error', status=400, safe=False)

def subspaces(request, spaceid=None):
    if request.method == 'GET':
        print(spaceid)
        if spaceid!=None:
            #data = JSONParser().parse(request)
            #serializer = SpaceSerializer(data=data,partial=True)
            plants = SubSpace.objects.filter(sub_space_id=spaceid)
            serialize = api.serializers.SubSpaceSerializer(plants, many=True)
            return JsonResponse( serialize.data, status=200 ,safe=False)
        else:
            plants = SubSpace.objects.all()
            serialize = api.serializers.SubSpaceSerializer(plants, many=True)
            return JsonResponse( serialize.data, status=200 ,safe=False)
    elif request.method == 'PUT':
        print ('iii')
    return JsonResponse('error', status=400, safe=False)

def plans(request):
    if request.method == 'GET':
        print(request.META['QUERY_STRING'])
        query = (request.META['QUERY_STRING']).split('=')
        if query[0] == 'subspace':
            subspaceid = (query[1])
            dayplans = DayPlan.objects.filter(dayplan_sub=subspaceid)
        #data = JSONParser().parse(request)
        #serializer = SpaceSerializer(data=data,partial=True)
        #plants = SubSpace.objects.filter(sub_space_id=spaceid)
        serialize = api.serializers.DayPlanSerializer(dayplans, many=True)
        return JsonResponse( serialize.data , status=200 ,safe=False)
    elif request.method == 'PUT':
        print ('iii')


    return JsonResponse('error', status=400, safe=False)

def irrigations(request):
    if request.method == 'GET':
        print(request.META['QUERY_STRING'])
        query = (request.META['QUERY_STRING']).split('=')
        if query[0] == 'subspace':
            print('é isso evaristo')
            subspaceid = (query[1])
            dayplans = IrrigationTime.objects.filter(irrigation_time_sub=subspaceid)
        #data = JSONParser().parse(request)
        #serializer = SpaceSerializer(data=data,partial=True)
        #plants = SubSpace.objects.filter(sub_space_id=spaceid)
        serialize = IrrigationTimeSerializer(dayplans, many=True)
        return JsonResponse( serialize.data , status=200 ,safe=False)
    elif request.method == 'PUT':
        print ('iii')


    return JsonResponse('error', status=400, safe=False)

def reads(request):
    if request.method == 'GET':
        #print(request.META['QUERY_STRING'])
        #query = (request.META['QUERY_STRING']).split('=')
        #if query[0] == 'subspace':
        #    print('é isso evaristo')
        #    subspaceid = (query[1])
        #    dayplans = IrrigationTime.objects.filter(irrigation_time_sub=subspaceid)
        #data = JSONParser().parse(request)
        #serializer = SpaceSerializer(data=data,partial=True)
        #plants = SubSpace.objects.filter(sub_space_id=spaceid)
        reads = Read.objects.all()
        serialize = ReadSerializer(reads, many=True)
        return JsonResponse( serialize.data , status=200 ,safe=False)
    elif request.method == 'PUT':
        print ('iii')


    return JsonResponse('error', status=400, safe=False)


def sensors(request):
    if request.method == 'GET':
        #print(request.META['QUERY_STRING'])
        #query = (request.META['QUERY_STRING']).split('=')
        #if query[0] == 'subspace':
        #    print('é isso evaristo')
        #    subspaceid = (query[1])
        #    dayplans = IrrigationTime.objects.filter(irrigation_time_sub=subspaceid)
        sensores = Sensor.objects.all()
        serialize = SensorSerializer(sensores, many=True)
        return JsonResponse( serialize.data , status=200 ,safe=False)
    elif request.method == 'PUT':
        print ('iii')


    return JsonResponse('error', status=400, safe=False)

def embeddedsystems(request):
    if request.method == 'GET':
        #print(request.META['QUERY_STRING'])
        #query = (request.META['QUERY_STRING']).split('=')
        #if query[0] == 'subspace':
        #    print('é isso evaristo')
        #    subspaceid = (query[1])
        #    dayplans = IrrigationTime.objects.filter(irrigation_time_sub=subspaceid)
        embedded = EmbeddedSystem.objects.all()
        serialize = EmbeddedSystemSerializer(embedded, many=True)
        return JsonResponse( serialize.data , status=200 ,safe=False)
    elif request.method == 'PUT':
        print ('iii')


    return JsonResponse('error', status=400, safe=False)

def warnings(request):
    if request.method == 'GET':
        #print(request.META['QUERY_STRING'])
        #query = (request.META['QUERY_STRING']).split('=')
        #if query[0] == 'subspace':
        #    print('é isso evaristo')
        #    subspaceid = (query[1])
        #    dayplans = IrrigationTime.objects.filter(irrigation_time_sub=subspaceid)
        warnings = Warnings.objects.all()
        serialize = WarningsSerializer(warnings, many=True)
        return JsonResponse( serialize.data , status=200 ,safe=False)
    elif request.method == 'PUT':
        print ('iii')


    return JsonResponse('error', status=400, safe=False)






