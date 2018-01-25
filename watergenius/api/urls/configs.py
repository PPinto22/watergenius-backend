from django.urls import path

# /configs
from api.views.configs import CentralNodeConfigView, PropertyConfigView, SensorConfigView

urlpatterns = [
    path('properties/<int:propid>/', PropertyConfigView.as_view()),
    path('properties/<int:propid>/node/', CentralNodeConfigView.as_view()),
    path('sensors/<int:sensorid>/', SensorConfigView.as_view())
]