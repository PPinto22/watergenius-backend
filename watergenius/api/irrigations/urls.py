from django.urls import path

from . import views

# /plans
urlpatterns = [
    path('', views.plans, name='plans'),
    # TODO - etc...
]