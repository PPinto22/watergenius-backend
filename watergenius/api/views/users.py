from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.users import User, UserCreateSerializer, UserSerializer
from api.models import *

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
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)



def populate(request):
    
    try:
        a = User()
        a.email = "rui.rrua@gmail.com"
        a.password = "rui"
        a.first_name = "Rui"
        a.last_name = "Rua"
        a.save()
    except Exception as e:
        print(e)

    try:
        a = User()
        a.email = "rafa@gmail.com"
        a.password = "rafa"
        a.first_name = "Rafa"
        a.last_name = "Mota"
        a.save()
    except Exception as e:
        print(e)
  
    try:
        a = User()
        a.email = "freitas@gmail.com"
        a.password = "freitas"
        a.first_name = "Rui"
        a.last_name = "Freitas"
        a.save()
    except Exception as e:
        print(e)
    
    try:
        b = Property()
        b.prop_name = "casa do rafa"
        b.prop_description = "monte"
        b.prop_address = " churrascaria do rafa numero 6"
        b.prop_owner_id = "rafa@gmail.com"
        b.save()
    except Exception as e:
        print(e)

    try:
        b = Property()
        b.prop_name = "casa do rui"
        b.prop_description = "monte"
        b.prop_address = " rua do maior de montalegre"
        b.prop_owner_id = "rui.rrua@gmail.com"
        b.save()
    except Exception as e:
        print(e)
    
    try:
        c = UserManagesProperty()
        c.user_id_id = "rafa@gmail.com"
        c.prop_id_id = 1
        c.save()
    except Exception as e:
        print(e)

    try:
        c = UserManagesProperty()
        c.user_id_id = "rui.rrua@gmail.com"
        c.prop_id_id = 1
        c.save()
    except Exception as e:
        print(e)

    try:
        c = UserManagesProperty()
        c.user_id_id = "rui.rrua@gmail.com"
        c.prop_id_id = 2
        c.save()
    except Exception as e:
        print(e)

    try:
        b = Property()
        b.prop_name = "casa do pinto"
        b.prop_description = "monte"
        b.prop_address = " rua do maior da terra dele"
        b.prop_owner_id = "pinto@gmail.com"
        b.save()
    except Exception as e:
        print(e)

    try:
        c = UserManagesProperty()
        c.user_id_id = "pinto@gmail.com"
        c.prop_id_id = 3
        c.save()
    except Exception as e:
        print(e)

    try:
        e = PlantType()
        e.plant_type_name = "relva"
        e.save()
    except Exception as e:
        print(e)

    try:
        d = Space()
        d.space_name = "relvado 1"
        d.space_description = "relva da churrascaria"
        d.space_irrigation_hour = 11
        d.space_plant_type_id = 1
        d.space_property_id =1
        d.save()
    except Exception as e:
        print(e)

    try:
        d = Space()
        d.space_name = "relvado 2"
        d.space_description = "relva das traseiras"
        d.space_irrigation_hour = 11
        d.space_plant_type_id = 1
        d.space_property_id =1
        d.save()
    except Exception as e:
        print(e)

    try:
        rest = TimeRestrition()
        rest.time_begin = "2017-12-21T00:00:00Z"
        rest.time_duration = "00:22:00"
        rest.time_restrition_space = 1
        rest.save()
    except Exception as e:
        print(e)

    try:
        rest = TimeRestrition()
        rest.time_begin = "2017-12-29T00:00:00Z"
        rest.time_duration = "00:12:00"
        rest.time_restrition_space = 1
        rest.save()
    except Exception as e:
        print(e)
    
    try:
        f = SubSpace()
        f.sub_name = "SubEspaço 1"
        f.sub_description = "Ao lado da estatua do frango"
        f.sub_space_id_id = 1
        f.save()
    except Exception as e:
        print(e)

    try:
        f = SubSpace()
        f.sub_name = "SubEspaço 2"
        f.sub_description = "Ao lado da estatua do rafa"
        f.sub_space_id_id = 2
        f.save()
    except Exception as e:
        print(e)

    try:
        d = Space()
        d.space_name = "relvado 2"
        d.space_description = "relva das traseiras"
        d.space_irrigation_hour = 22
        d.space_plant_type_id = 1
        d.space_property_id =2
        d.save()
    except Exception as e:
        print(e)

    try:
        f = SubSpace()
        f.sub_name = "SubEspaço 1"
        f.sub_description = " relvado das traseiras"
        f.sub_space_id_id = 1
        f.save()
    except Exception as e:
        print(e)

    try:
        h = Localization()
        h.local_long = 120
        h.local_lat = 130
        h.save()
    except Exception as e:
        print(e)

    try:
        h = Localization()
        h.local_long = 1201
        h.local_lat = 1301
        h.save()
    except Exception as e:
        print(e)
    try:
        irrigation = IrrigationTime()
        irrigation.irrigation_time_date = "2017-12-21T00:00:00Z"
        irrigation.irrigation_time_qtd = 10
        irrigation.irrigation_time_sub = 1
        irrigation.save()
    except Exception as e:
        print(e)
    try:
        g = CentralNode()
        g.node_ip = "127.0.0.1"
        g.node_local_id = 1
        g.node_property_id = 1
        g.save()
    except Exception as e:
        print(e)
    try:
        g = CentralNode()
        g.node_ip = "127.0.1.1"
        g.node_local_id = 2
        g.node_property_id = 2
        g.save()
    except Exception as e:
        print(e)

    try:
        i = EmbeddedSystem()
        i.esys_state = 1
        i.esys_local_id = 2
        i.esys_sub_id = 1 
        i.esys_name = "arduino 1"
        i.esys_network_pass = "laura"
        i.save()
    except Exception as e:
        print(e)

    try:
        i = EmbeddedSystem()
        i.esys_state = 1
        i.esys_local_id = 2
        i.esys_sub_id = 1 
        i.esys_name = "arduino 1"
        i.esys_network_pass = "laura"
        i.save()
    except Exception as e:
        print(e)
    
    try:
        i = EmbeddedSystem()
        i.esys_state = 1
        i.esys_local_id = 1
        i.esys_sub_id = 2 
        i.esys_name = "arduino 2"
        i.esys_network_pass = "laurinda"
        i.save()
    except Exception as e:
        print(e)
    
    try:
        tipo = SensorType()
        tipo_sensor_type_name = "Humidade"
        tipo.save()
    except Exception as e:
        print(e)
    
    try:
        sensor = Sensor()
        sensor.sensor_state = 0
        sensor.sensor_timerate = 10
        sensor.sensor_depth = 20
        sensor.sensor_sub_id = 1
        sensor.sensor_type_id = 1
        sensor.save()
    except Exception as e:
        print(e)
    
    try:
        sensor = Sensor()
        sensor.sensor_state = 1
        sensor.sensor_timerate = 101
        sensor.sensor_depth = 201
        sensor.sensor_sub_id = 2
        sensor.sensor_type_id = 1
        sensor.save()
    except Exception as e:
        print(e)

    try:
        read = ReadType()
        read.read_type_name = "leitura"
        read.read_type_units= "ua"
        read.read_type_coef= 10
        read_type_sensor_id = 1
        read.save()
    except Exception as e:
        print(e)

    try:
        read = ReadType()
        read.read_type_name = " leitura"
        read.read_type_units= "ua"
        read.read_type_coef= 10
        read_type_sensor_id = 2
        read.save()
    except Exception as e:
        print(e)
    try:
        read = ReadType()
        read.read_type_name = " leitura"
        read.read_type_units= "ua"
        read.read_type_coef= 10
        read_type_sensor_id = 1
        read.save()
    except Exception as e:
        print(e)
    try:
        day = DayPlan()
        day.dayplan_time = "2017-12-21T00:00:00Z"
        day.dayplan_water_qtd = 2
        day.dayplan_sub = 1
        day.save()
    except Exception as e:
        print(e)
    try:
        day = DayPlan()
        day.dayplan_time = "2017-12-22T00:03:00Z"
        day.dayplan_water_qtd = 21
        day.dayplan_sub = 2
        day.save()
    except Exception as e:
        print(e)
    try:
        rd = Read()
        rd.read_value = 100
        rd.read_dayplan_id =1
        rd.read_sensor_id = 1
        rd.read_type_id = 1
        rd.save()
    except Exception as e:
        print(e)
    try:
        rd = Read()
        rd.read_value = 100
        rd.read_dayplan_id =2
        rd.read_sensor_id = 2
        rd.read_type_id = 1
        rd.save()
    except Exception as e:
        print(e)
    

   


    

    



def userByMail(request, mail=None):
    
    if request.method =='POST':
        if(mail=='populate@gmail.com'):
            populate(request)
            return JsonResponse("populei tudo", safe=False)
    if request.method == 'GET':
        print("eueu")
        # data = JSONParser().parse(request)
        user = User.objects.get(email=mail)
        serializer = UserSerializer(user, many=False)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        # editar user
        user = User.objects.get(email=mail)
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data, partial=True)
        print(serializer.is_valid())
        # assuming that serializer is valid. TODO
        if serializer.data['email'] == user.email:
            user.name = serializer.data['name']
            user.admin = serializer.data['admin']
            user.save()
            return JsonResponse(serializer.data, status=201)
    elif request.method == 'DELETE':
        user = User.objects.get(email=mail)
        print(user)
        if user:
            user.delete()
            return JsonResponse('OK', status=200, safe=False)

    return JsonResponse(serializer.errors, status=400)