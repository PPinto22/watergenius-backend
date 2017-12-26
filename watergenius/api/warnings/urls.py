from django.urls import path

from . import views

# /warnings
urlpatterns = [
    path('', views.warnings, name='warnings'),
    # TODO - etc...
]