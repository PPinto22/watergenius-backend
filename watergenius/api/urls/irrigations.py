from django.urls import path

from api.views.irrigations import IrrigationTimeListView, IrrigationTimeDetailView

# /irrigations
urlpatterns = [
    path('', IrrigationTimeListView.as_view(), name='irrigations'),
    path('<int:irrigationid>/',IrrigationTimeDetailView.as_view(), name='irrigation'),
]