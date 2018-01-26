import errno
import json

import os
import re
import shutil
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from api.models import Property, Sensor, CentralNode
from api.views.sensors import getSensorsOfProperty


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
        prop = Property.objects.get(prop_id=propid)
        if os.path.exists(propDir(prop)):
            shutil.rmtree(propDir(prop))
        savePropertyConfig(request, prop)

        shutil.make_archive(propFile(prop, full_path=True, include_extension=False), 'zip', nodeDir(prop))

        print(propFile(prop, full_path=True))
        with open(propFile(prop, full_path=True), 'rb') as zipFile:
            response = HttpResponse(zipFile, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename={0}'.format(propFile(prop))
            return response


# Global functions
def getCentralNodeConfig(request, prop):
    # FIXME - Remover este caso
    token = request.auth
    if token is not None:
        token = token.decode("utf-8")

    config = {
        'serverURL': 'https://watergenius-backend.herokuapp.com/',
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
    createDirectoryIfNotExists(nodeDir(prop))
    with open(nodeFile(prop, full_path=True), 'w') as file:
        file.write(config)


def saveSensorConfig(sensor, config):
    createDirectoryIfNotExists(sensorDir(sensor))
    with open(sensorFile(sensor, full_path=True), 'w') as file:
        file.write(config)


def savePropertyConfig(request, prop):
    createDirectoryIfNotExists(propDir(prop))

    nodeConfig = getCentralNodeConfig(request, prop)
    saveCentralNodeConfig(prop, nodeConfig)

    node = CentralNode.objects.get(node_property=prop.prop_id)
    sensors = getSensorsOfProperty(prop)
    with open('api/static/sensor.ino', 'r') as file:
        inoFile = file.read()

    for sensor in sensors:
        sensorConfig = getSensorConfig(sensor, file_content=inoFile,
                                       ssid=node.node_network_name,
                                       pw=node.node_network_password)
        saveSensorConfig(sensor, sensorConfig)


def propDir(prop):
    return 'api/static/properties/{0}/'.format(prop.prop_id)

def nodeDir(prop):
    return propDir(prop)+'data/'

def sensorDir(sensor):
    subspace = sensor.sensor_esys.esys_sub
    space = subspace.sub_space_id
    prop = space.space_property
    return nodeDir(prop)+'/space{1}_{2}/subspace{3}_{4}/' \
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
        path += nodeDir(prop)
    return path + 'node{0}_{1}.json'.format(prop.prop_id, safe(prop.prop_name))


def propFile(prop, full_path=False, include_extension=True):
    path = ''
    if full_path:
        path = propDir(prop)
    extension = ''
    if include_extension:
        extension = '.zip'
    return path + 'property{0}_{1}'.format(prop.prop_id, safe(prop.prop_name) + extension)


def safe(unsafeFileName):
    return "".join([c for c in unsafeFileName.lower() if re.match(r'\w', c)])


def createDirectoryIfNotExists(dirname):
    if not os.path.exists(dirname):
        try:
            os.makedirs(os.path.dirname(dirname))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
