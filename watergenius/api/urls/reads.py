from django.urls import path

from api.views.reads import reads

# /reads
urlpatterns = [
    path('', reads, name='reads'),
    # TODO - etc...
]