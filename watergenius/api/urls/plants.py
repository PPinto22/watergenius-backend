from django.urls import path

from api.views.plants import plants

# /plants
urlpatterns = [
    path('', plants)
]