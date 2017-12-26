from django.urls import path

from . import views

# /subspaces
urlpatterns = [
    path('', views.embeddedsystems, name='embeddedsystems'),
    # TODO - etc...
]