from django.urls import path

from api.views.plants import PlantsListView

# /plants
urlpatterns = [
    path('', PlantsListView.as_view())
]