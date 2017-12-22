from django.urls import include, path
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view()),
    path('auth', obtain_jwt_token),

    path('users', views.UserView.as_view()),
    path('properties/',include('api.props')),
    path('spaces/',include('api.spaces')),
    path('plants/',include('api.plants')),
    #path('subspaces/',include('api.subspaces')),
    path('subspaces/<int:spaceid>/',include('api.subspaces')),
    path('plans/',include('api.plans')),
]