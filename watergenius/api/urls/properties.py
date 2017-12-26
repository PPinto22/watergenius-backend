from django.urls import path, re_path

from api.views.properties import properties, propertiesManagers, propertiesNode

# /properties
urlpatterns = [
    path('', properties, name='properties'),
    path('<int:propid>/', properties, name='property'), # TODO funcao separada?

    path('<int:propid>/node/', propertiesNode, name='propertiesNode'),

    re_path(r'^(?P<propid>\w+)/managers/(?P<managerid>\w{1,50}[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$',
            propertiesManagers, name='propertiesManagers'),
    path('<int:propid>/managers/', propertiesManagers, name='propertiesManagers'),
]
