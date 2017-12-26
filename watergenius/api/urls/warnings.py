from django.urls import path

from api.views.warnings import warnings

# /warnings
urlpatterns = [
    path('', warnings, name='warnings'),
]