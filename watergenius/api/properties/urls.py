from django.urls import include, path, re_path

from . import views

# /properties
urlpatterns = [
    path('', views.properties, name='properties'),
    path('/<int:propid>/node', views.propertiesNode, name='propertiesNode'),
    re_path(r'^/(?P<propid>\w+)/managers/(?P<managerid>\w{1,50}[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$',
            views.propertiesManagers, name='propertiesManagers'),
    path('/<int:propid>/managers', views.propertiesManagers, name='propertiesManagers'),
    path('/properties/<int:propid>',include('api.props')),
]