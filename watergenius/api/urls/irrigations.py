from django.urls import path

from api.views.irrigations import irrigations

# /irrigations
urlpatterns = [
    path('', irrigations, name='irrigations'),
    # TODO - etc...
]