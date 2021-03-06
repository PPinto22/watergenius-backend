from django.core.management import call_command
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *

from api.models import *


class PopulateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            a = User()
            a.email = "rui.rrua@gmail.com"
            a.set_password("rui")
            a.first_name = "Rui"
            a.last_name = "Rua"
            a.save()
        except Exception as e:
            print(e)

        try:
            a = User()
            a.email = "pinto@gmail.com"
            a.set_password("pinto")
            a.first_name = "Pedro"
            a.last_name = "Pinto"
            a.save()
        except Exception as e:
            print(e)

        try:
            a = User()
            a.email = "rafa@gmail.com"
            a.set_password("rafa")
            a.first_name = "Rafa"
            a.last_name = "Mota"
            a.save()
        except Exception as e:
            print(e)

        try:
            a = User()
            a.email = "freitas@gmail.com"
            a.set_password("freitas")
            a.first_name = "Rui"
            a.last_name = "Freitas"
            a.save()
        except Exception as e:
            print(e)
        try:
            a = User()
            a.email = "carlos@gmail.com"
            a.set_password("carlos")
            a.first_name = "Carlos"
            a.last_name = "Castro"
            a.save()
        except Exception as e:
            print(e)
        try:
            a = User()
            a.email = "ribeiro@gmail.com"
            a.set_password("ribeiro")
            a.first_name = "Hugo"
            a.last_name = "Ribeiro"
            a.save()
        except Exception as e:
            print(e)

        try:
            a = User()
            a.email = "joao@gmail.com"
            a.set_password("joao")
            a.first_name = "Joao"
            a.last_name = "Silva"
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
            b = Property()
            b.prop_name = "casa do rua"
            b.prop_description = "monte"
            b.prop_address = " rua do maior de montalegre"
            b.prop_owner_id = "rui.rrua@gmail.com"
            b.save()
        except Exception as e:
            print(e)

        try:
            b = Property()
            b.prop_name = "casa do carlos"
            b.prop_description = "monte"
            b.prop_address = " rua do maior de castro"
            b.prop_owner_id = "carlos@gmail.com"
            b.save()
        except Exception as e:
            print(e)

        try:
            b = Property()
            b.prop_name = "casa de aboim"
            b.prop_description = "monte"
            b.prop_address = " rua do maior de castro"
            b.prop_owner_id = "rafa@gmail.com"
            b.save()
        except Exception as e:
            print(e)

        try:
            c = UserManagesProperty()
            c.user_id = "rafa@gmail.com"
            c.prop_id = 1
            c.save()
        except Exception as e:
            print(e)

        try:
            c = UserManagesProperty()
            c.user_id = "rui.rrua@gmail.com"
            c.prop_id = 1
            c.save()
        except Exception as e:
            print(e)
        try:
            c = UserManagesProperty()
            c.user_id = "rafa@gmail.com"
            c.prop_id = 3
            c.save()
        except Exception as e:
            print(e)

        try:
            c = UserManagesProperty()
            c.user_id = "rui.rrua@gmail.com"
            c.prop_id = 4
            c.save()
        except Exception as e:
            print(e)

        try:
            c = UserManagesProperty()
            c.user_id = "joao@gmail.com"
            c.prop_id = 1
            c.save()
        except Exception as e:
            print(e)

        try:
            c = UserManagesProperty()
            c.user_id = "carlos@gmail.com"
            c.prop_id = 1
            c.save()
        except Exception as e:
            print(e)

        try:
            c = UserManagesProperty()
            c.user_id = "rui.rrua@gmail.com"
            c.prop_id = 3
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
            c.user_id = "pinto@gmail.com"
            c.prop_id = 2
            c.save()
        except Exception as e:
            print(e)

        # try:
        #     e = PlantType()
        #     e.plant_type_name = "relva"
        #     e.save()
        # except Exception as e:
        #     print(e)

        try:
            d = Space()
            d.space_name = "relvado 1"
            d.space_description = "relva da churrascaria"
            d.space_irrigation_hour = 11
            d.space_plant_type_id = "grass"
            d.space_property_id = 1
            d.save()
        except Exception as e:
            print(e)

        try:
            d = Space()
            d.space_name = "relvado 2"
            d.space_description = "relva das traseiras"
            d.space_irrigation_hour = 11
            d.space_plant_type_id = "grass"
            d.space_property_id = 1
            d.save()
        except Exception as e:
            print(e)

        try:
            d = Space()
            d.space_name = "relvado 12"
            d.space_description = "relva daqui"
            d.space_irrigation_hour = 11
            d.space_plant_type_id = "grass"
            d.space_property_id = 2
            d.save()
        except Exception as e:
            print(e)

        try:
            d = Space()
            d.space_name = "aaa 2"
            d.space_description = "relva do lado"
            d.space_irrigation_hour = 8
            d.space_plant_type_id = "grass"
            d.space_property_id = 3
            d.save()
        except Exception as e:
            print(e)

        try:
            d = Space()
            d.space_name = "a 2"
            d.space_description = "relva do fundo"
            d.space_irrigation_hour = 13
            d.space_plant_type_id = "grass"
            d.space_property_id = 4
            d.save()
        except Exception as e:
            print(e)

        try:
            rest = TimeRestriction()
            rest.time_restriction_begin = "2017-12-21T00:00:00Z"
            rest.time_restriction_end = "2017-12-21T00:22:00Z"
            rest.time_restriction_space = Space.objects.get(space_id=2)
            rest.save()
        except Exception as e:
            print(e)

        try:
            rest = TimeRestriction()
            rest.time_restriction_begin = "2017-12-29T00:00:00Z"
            rest.time_restriction_end = "2017-12-29T00:12:00Z"
            rest.time_restriction_space = Space.objects.get(space_id=1)
            rest.save()
        except Exception as e:
            print(e)
        try:
            rest = TimeRestriction()
            rest.time_restriction_begin = "2017-12-23T00:00:00Z"
            rest.time_restriction_end = "2017-12-23T00:23:00Z"
            rest.time_restriction_space = Space.objects.get(space_id=3)
            rest.save()
        except Exception as e:
            print(e)

        try:
            rest = TimeRestriction()
            rest.time_restriction_begin = "2017-12-25T00:00:00Z"
            rest.time_restriction_end = "2017-12-25T00:13:00Z"
            rest.time_restriction_space = Space.objects.get(space_id=4)
            rest.save()
        except Exception as e:
            print(e)

        try:
            rest = TimeRestriction()
            rest.time_restriction_begin = "2017-12-23T00:00:00Z"
            rest.time_restriction_end = "2017-12-23T00:22:00Z"
            rest.time_restriction_space = Space.objects.get(space_id=2)
            rest.save()
        except Exception as e:
            print(e)

        try:
            rest = TimeRestriction()
            rest.time_restriction_begin = "2017-12-29T00:00:00Z"
            rest.time_restriction_end = "2017-12-29T00:11:00Z"
            rest.time_restriction_space = Space.objects.get(space_id=1)
            rest.save()
        except Exception as e:
            print(e)

        try:
            rest = TimeRestriction()
            rest.time_restriction_begin = "2017-12-21T00:00:00Z"
            rest.time_restriction_end = "2017-12-21T00:22:00Z"
            rest.time_restriction_space = Space.objects.get(space_id=4)
            rest.save()
        except Exception as e:
            print(e)

        try:
            rest = TimeRestriction()
            rest.time_restriction_begin = "2017-12-29T00:00:00Z"
            rest.time_restriction_end = "2017-12-29T00:12:00Z"
            rest.time_restriction_space = Space.objects.get(space_id=3)
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
            f.sub_space_id_id = 3
            f.save()
        except Exception as e:
            print(e)

        try:
            f = SubSpace()
            f.sub_name = "SubEspaço 3"
            f.sub_description = "Ao lado da estatua do tio"
            f.sub_space_id_id = 4
            f.save()
        except Exception as e:
            print(e)

        try:
            f = SubSpace()
            f.sub_name = "SubEspaço 23"
            f.sub_description = "Ao lado da estatua do ze"
            f.sub_space_id_id = 3
            f.save()
        except Exception as e:
            print(e)

        try:
            d = Space()
            d.space_name = "relvado 3"
            d.space_description = "relva do lago"
            d.space_irrigation_hour = 2
            d.space_plant_type_id = "grass"
            d.space_property_id = 4
            d.save()
        except Exception as e:
            print(e)

        try:
            f = SubSpace()
            f.sub_name = "SubEspa22222ço 23"
            f.sub_description = "Ao lado da1 estatua do ze"
            f.sub_space_id_id = 3
            f.save()
        except Exception as e:
            print(e)

        try:
            d = Space()
            d.space_name = "relv222ado 3"
            d.space_description = "relva do l222ago"
            d.space_irrigation_hour = 2
            d.space_plant_type_id = "grass"
            d.space_property_id = 4
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
            irrigation = IrrigationTime()
            irrigation.irrigation_time_date = "2017-12-21T00:00:00Z"
            irrigation.irrigation_time_qty = 10
            irrigation.irrigation_time_sub = SubSpace.objects.get(sub_id=1)
            irrigation.save()
        except Exception as e:
            print(e)
        try:
            irrigation = IrrigationTime()
            irrigation.irrigation_time_date = "2017-12-21T00:00:00Z"
            irrigation.irrigation_time_qty = 10
            irrigation.irrigation_time_sub = SubSpace.objects.get(sub_id=1)
            irrigation.save()
        except Exception as e:
            print(e)
        try:
            irrigation = IrrigationTime()
            irrigation.irrigation_time_date = "2018-01-02T00:00:00Z"
            irrigation.irrigation_time_qty = 10
            irrigation.irrigation_time_sub = SubSpace.objects.get(sub_id=4)
            irrigation.save()
        except Exception as e:
            print(e)
        try:
            irrigation = IrrigationTime()
            irrigation.irrigation_time_date = "2018-12-03T00:00:00Z"
            irrigation.irrigation_time_qty = 10
            irrigation.irrigation_time_sub = SubSpace.objects.get(sub_id=2)
            irrigation.save()
        except Exception as e:
            print(e)
        try:
            irrigation = IrrigationTime()
            irrigation.irrigation_time_date = "2018-01-02T00:00:00Z"
            irrigation.irrigation_time_qty = 10
            irrigation.irrigation_time_sub = SubSpace.objects.get(sub_id=4)
            irrigation.save()
        except Exception as e:
            print(e)
        try:
            irrigation = IrrigationTime()
            irrigation.irrigation_time_date = "2018-12-03T00:00:00Z"
            irrigation.irrigation_time_qty = 10
            irrigation.irrigation_time_sub = SubSpace.objects.get(sub_id=3)
            irrigation.save()
        except Exception as e:
            print(e)
        try:
            g = CentralNode()
            g.node_ip = "127.0.0.1"
            # g.node_local_id = 1
            g.node_property_id = 1
            g.node_network_name = "LAN"
            g.node_network_password = "password"
            g.save()
        except Exception as e:
            print(e)
        try:
            g = CentralNode()
            g.node_ip = "127.0.1.1"
            # g.node_local_id = 2
            g.node_property_id = 2
            g.node_network_name = "LAN"
            g.node_network_password = "password"
            g.save()
        except Exception as e:
            print(e)

        try:
            g = CentralNode()
            g.node_ip = "127.10.0.1"
            # g.node_local_id = 1
            g.node_property_id = 3
            g.node_network_name = "LAN"
            g.node_network_password = "password"
            g.save()
        except Exception as e:
            print(e)
        try:
            g = CentralNode()
            g.node_ip = "127.12.1.1"
            # g.node_local_id = 2
            g.node_property_id = 4
            g.node_network_name = "LAN"
            g.node_network_password = "password"
            g.save()
        except Exception as e:
            print(e)

        try:
            i = EmbeddedSystem()
            i.esys_state = 1
            # i.esys_local_id = 2
            i.esys_sub_id = 1
            i.esys_name = "arduino 1"
            i.save()
        except Exception as e:
            print(e)

        try:
            i = EmbeddedSystem()
            i.esys_state = 1
            # i.esys_local_id = 2
            i.esys_sub_id = 1
            i.esys_name = "arduino 1"
            i.save()
        except Exception as e:
            print(e)

        try:
            i = EmbeddedSystem()
            i.esys_state = 1
            # i.esys_local_id = 1
            i.esys_sub_id = 2
            i.esys_name = "arduino 2"
            i.save()
        except Exception as e:
            print(e)

        try:
            i = EmbeddedSystem()
            i.esys_state = 1
            # i.esys_local_id = 2
            i.esys_sub_id = 2
            i.esys_name = "aro 15"
            i.save()
        except Exception as e:
            print(e)

        try:
            i = EmbeddedSystem()
            i.esys_state = 0
            # i.esys_local_id = 2
            i.esys_sub_id = 3
            i.esys_name = "arduino 11"
            i.save()
        except Exception as e:
            print(e)

        try:
            i = EmbeddedSystem()
            i.esys_state = 1
            # i.esys_local_id = 1
            i.esys_sub_id = 1
            i.esys_name = "arduino 12"
            i.save()
        except Exception as e:
            print(e)

        # try:
        #     tipo = SensorType()
        #     tipo_sensor_type_name = "Humidade"
        #     tipo.save()
        # except Exception as e:
        #     print(e)

        try:
            sensor = Sensor()
            sensor.sensor_state = 0
            sensor.sensor_timerate = 10
            sensor.sensor_depth = 20
            sensor.sensor_esys_id = 1
            sensor.sensor_type_id = "humidity"
            sensor.save()
        except Exception as e:
            print(e)

        try:
            sensor = Sensor()
            sensor.sensor_state = 1
            sensor.sensor_timerate = 101
            sensor.sensor_depth = 201
            sensor.sensor_esys_id = 2
            sensor.sensor_type_id = "humidity"
            sensor.save()
        except Exception as e:
            print(e)

        try:
            sensor = Sensor()
            sensor.sensor_state = 1
            sensor.sensor_timerate = 13
            sensor.sensor_depth = 202
            sensor.sensor_esys_id = 2
            sensor.sensor_type_id = "humidity"
            sensor.save()
        except Exception as e:
            print(e)

        try:
            sensor = Sensor()
            sensor.sensor_state = 1
            sensor.sensor_timerate = 101
            sensor.sensor_depth = 201
            sensor.sensor_esys_id = 2
            sensor.sensor_type_id = "humidity"
            sensor.save()
        except Exception as e:
            print(e)

        try:
            sensor = Sensor()
            sensor.sensor_state = 0
            sensor.sensor_timerate = 210
            sensor.sensor_depth = 2
            sensor.sensor_esys_id = 3
            sensor.sensor_type_id = "humidity"
            sensor.save()
        except Exception as e:
            print(e)

        try:
            sensor = Sensor()
            sensor.sensor_state = 1
            sensor.sensor_timerate = 1011
            sensor.sensor_depth = 1
            sensor.sensor_esys_id = 4
            sensor.sensor_type_id = "humidity"
            sensor.save()
        except Exception as e:
            print(e)

        return Response("OK", HTTP_200_OK)

class PopulateViewV2(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        call_command('loaddata', 'tests/users.json', app_label='api')
        call_command('loaddata', 'tests/properties.json', app_label='api')
        call_command('loaddata', 'tests/spaces.json', app_label='api')
        call_command('loaddata', 'tests/subspaces.json', app_label='api')
        call_command('loaddata', 'tests/esys.json', app_label='api')
        call_command('loaddata', 'tests/sensors.json', app_label='api')
        call_command('loaddata', 'tests/reads.json', app_label='api')
        call_command('loaddata', 'tests/irrigations.json', app_label='api')
        call_command('loaddata', 'tests/dayplans.json', app_label='api')
        return Response('OK', HTTP_200_OK)