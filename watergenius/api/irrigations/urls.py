from django.urls import path

from . import views

# /irrigations
urlpatterns = [
    path('', views.irrigations, name='irrigations'),
    # TODO - etc...
]