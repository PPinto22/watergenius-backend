from django.urls import path

from api.views.sensors import sensors

# /sensors
urlpatterns = [
    path('', sensors, name='sensors'),
    # TODO - etc...
]