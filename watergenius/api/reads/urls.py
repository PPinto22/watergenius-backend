from django.urls import path

from . import views

# /reads
urlpatterns = [
    path('', views.reads, name='reads'),
    # TODO - etc...
]