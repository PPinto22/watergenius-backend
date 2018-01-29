from django.urls import path

from api.views.plants import PlantsListView, PlantDetailView

# /plants
urlpatterns = [
    path('', PlantsListView.as_view()),
    path('<slug:plantid>/', PlantDetailView.as_view())
]