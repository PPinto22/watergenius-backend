from django.urls import path

from . import views

# /plants
urlpatterns = [
    path('', views.plants())
]