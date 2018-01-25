import errno
import json

import os
import re
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from api.models import Property, Sensor, CentralNode


class CentralNodeConfigView(APIView):
    permission_classes = [AllowAny]  # FIXME - Remover esta linha

    def get(self, request, propid):
        prop = Property.objects.get(prop_id=propid)
        config = getCentralNodeConfig(request, prop)
        saveCentralNodeConfig(prop, config)

        with open(nodeFile(prop, full_path=True), 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(nodeFile(prop))
        return response


class SensorConfigView(APIView):
    permission_classes = [AllowAny]  # FIXME - Remover esta linha

    def get(self, request, sensorid):
        sensor = Sensor.objects.get(sensor_id=sensorid)
        prop = sensor.sensor_esys.esys_sub.sub_space_id.space_property
        config = getSensorConfig(sensor)
        saveSensorConfig(sensor, config)

        with open(sensorFile(sensor, full_path=True), 'rb') as file:
            response = HttpResponse(file.read(), content_type='text/ino')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(sensorFile(sensor))
        return response


class PropertyConfigView(APIView):
    permission_classes = [AllowAny]  # FIXME - Remover esta linha

    def get(self, request, propid):
        # config = getCentralNodeConfig(request, propid)
        # saveCentralNodeConfig(propid, config)
        pass


# Global functions
def getCentralNodeConfig(request, prop):
    # FIXME - Remover este caso
    token = request.auth
    if token is not None:
        token = token.decode("utf-8")

    config = {
        'serverURL': '192.168.1.39:8000',  # FIXME
        'user': prop.prop_owner.email,
        'token': token,  # FIXME - Token pode ser do admin e nao do proprietario
        'property': str(prop.prop_id)
    }
    return json.dumps(config, indent=4)


def getSensorConfig(sensor, file_content=None, ssid=None, pw=None):
    if file_content is None:
        with open('api/static/sensor.ino', 'r') as file:
            file_content = file.read()
    if ssid is None or pw is None:
        prop = sensor.sensor_esys.esys_sub.sub_space_id.space_property
        node = CentralNode.objects.get(node_property=prop.prop_id)
        ssid = node.node_network_name
        pw = node.node_network_password

    #  TODO - Replace in a single pass
    config = re.sub(r'\d* */\*NODEID\*/', str(sensor.sensor_esys.esys_id), file_content)
    config = re.sub(r'\d* */\*SENSORID\*/', str(sensor.sensor_id), config)
    config = re.sub(r'(\"[^"]*\")? */\*SSID\*/', '\"' + ssid + '\"', config)
    config = re.sub(r'(\"[^"]*\")? */\*PW\*/', '\"' + pw + '\"', config)
    config = re.sub(r'\d* */\*TIMERATE\*/', str(sensor.sensor_timerate), config)
    return config


def saveCentralNodeConfig(prop, config):
    createDirectoryIfNotExists(propDir(prop))
    with open(nodeFile(prop, full_path=True), 'w') as file:
        file.write(config)


def saveSensorConfig(sensor, config):
    createDirectoryIfNotExists(sensorDir(sensor))
    with open(sensorFile(sensor, full_path=True), 'w') as file:
        file.write(config)


def savePropertyConfig(propid):
    createDirectoryIfNotExists('api/static/properties/{0}/...'.format(propid))
    # TODO


def propDir(prop):
    return 'api/static/properties/{0}/'.format(prop.prop_id)


def sensorDir(sensor):
    subspace = sensor.sensor_esys.esys_sub
    space = subspace.sub_space_id
    prop = space.space_property
    return 'api/static/properties/{0}/space{1}_{2}/subspace{3}_{4}/' \
        .format(prop.prop_id, space.space_id, safe(space.space_name),
                subspace.sub_id, safe(subspace.sub_name))


def sensorFile(sensor, full_path=False):
    path = ''
    if full_path:
        path += sensorDir(sensor)
    return path + 'sensor{0}_{1}.ino'.format(sensor.sensor_id, safe(sensor.sensor_name))


def nodeFile(prop, full_path=False):
    path = ''
    if full_path:
        path += propDir(prop)
    return path + 'node{0}_{1}.json'.format(prop.prop_id, safe(prop.prop_name))


def safe(unsafeFileName):
    return "".join([c for c in unsafeFileName.lower() if re.match(r'\w', c)])


def createDirectoryIfNotExists(dirname):
    if not os.path.exists(os.path.dirname(dirname)):
        try:
            os.makedirs(os.path.dirname(dirname))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
