from django.urls import include, path , re_path
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view()),
    path('auth', obtain_jwt_token),
    path('users', views.UserView.as_view()),
    #re_path('(?P<mail>\w{1,50}[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/', views.usersMail, ),
    path('properties/',include('api.props')),
    path('properties/<int:propid>/',include('api.props')),
    path('spaces/',include('api.spaces')),
    path('spaces/<int:spaceid>/',include('api.spaces')),
    path('spaces/<int:spaceid>/restritions/<int:resid>',include('api.spaces')),
    path('plants/',include('api.plants')),
    path('subspaces/',include('api.subspaces')),
    path('subspaces/<int:spaceid>/',include('api.subspaces')),
    path('plans',include('api.plans')),
    path('sensors', include('api.sensors')),
    path('reads', include('api.reads')),
    path('embeddedsys', include('api.embedded')),
    path('warnings', include('api.warnings')),
]