from django.urls import path, re_path

from api.views.properties import PropertyManagersListView, PropertyManagerDetailView, PropertiesListView, \
    PropertyDetailView, PropertyNodeView

# /properties
urlpatterns = [
    path('', PropertiesListView.as_view(), name='properties'),
    path('<int:propid>/', PropertyDetailView.as_view(), name='property'),

    path('<int:propid>/node/', PropertyNodeView.as_view(), name='propertyNode'),

    re_path(r'^(?P<propid>\w+)/managers/(?P<managerid>\w{1,50}[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$',
            PropertyManagerDetailView.as_view(), name='propertyManagerDetail'),
    path('<int:propid>/managers/', PropertyManagersListView.as_view(), name='propertyManagers'),
]
