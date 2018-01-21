from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token

from api.views.users import RegisterView
from api.views.populate import PopulateView, PopulateViewV2
from watergenius import settings

urlpatterns = [
    path('auth/', obtain_jwt_token),
    path('register/', RegisterView.as_view()),
    path('users/', include('api.urls.users')),
    path('properties/', include('api.urls.properties')),
    path('spaces/', include('api.urls.spaces')),
    path('plants/',include('api.urls.plants')),
    path('subspaces/',include('api.urls.subspaces')),
    path('irrigations/',include('api.urls.irrigations')),
    path('plans/', include('api.urls.plans')),
    path('sensors/', include('api.urls.sensors')),
    path('reads/', include('api.urls.reads')),
    path('embeddedsys/', include('api.urls.embeddedsys')),
    path('warnings/', include('api.urls.warnings')),
]

if settings.DEBUG:
    urlpatterns += [
        path('populate/', PopulateView.as_view()),
        path('populate/v2/', PopulateViewV2.as_view()),
    ]