from django.urls import path

from . import views

# /subspaces
urlpatterns = [
    path('', views.subspaces, name='subspaces'),
    # TODO - etc...
]