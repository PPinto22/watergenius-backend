from django.urls import path

from . import views

# /embeddedsys
urlpatterns = [
    path('', views.embeddedsystems, name='embeddedsystems'),
    # TODO - etc...
]