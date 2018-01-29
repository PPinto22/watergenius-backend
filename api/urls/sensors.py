from django.urls import path

from api.views.sensors import SensorsListView, SensorDetailView

# /sensors
urlpatterns = [
    path('', SensorsListView.as_view(), name='sensors'),
    path('<int:sensid>/', SensorDetailView.as_view(), name='sensor'),
]