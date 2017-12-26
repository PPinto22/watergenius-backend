from django.urls import include, path
from rest_framework_jwt.views import obtain_jwt_token

from api.users.views import RegisterView

urlpatterns = [
    path('auth', obtain_jwt_token),
    path('register', RegisterView.as_view()),
    path('users', include('api.users.urls')),
    path('properties', include('api.properties.urls')),
    path('spaces', include('api.spaces.urls')),
    path('plants',include('api.plants.urls')),
    path('subspaces',include('api.subspaces.urls')),
    path('plans',include('api.plans.urls')),
    path('sensors', include('api.sensors.urls')),
    path('reads', include('api.reads.urls')),
    path('embeddedsys', include('api.embedded.urls')),
    path('warnings', include('api.warnings.urls')),
]
