from django.urls import path

from api.views.sensors import sensors

# /sensors
urlpatterns = [
    path('', sensors, name='sensors'),
    path('<int:sensid>/', sensors, name='sensor') # TODO - funcao separada?
]