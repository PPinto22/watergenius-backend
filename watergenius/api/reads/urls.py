from django.urls import path

from . import views

# /sensors
urlpatterns = [
    path('', views.sensors, name='sensors'),
    # TODO - etc...
]