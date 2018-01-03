from django.urls import path

from api.views.irrigations import IrrigationsListView, IrrigationDetailView

# /irrigations
urlpatterns = [
    path('', IrrigationsListView.as_view(), name='irrigations'),
    path('<int:irrigationid>/', IrrigationDetailView.as_view(), name='irrigation'),
]