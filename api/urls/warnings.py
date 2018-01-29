from django.urls import path

from api.views.warnings import WarningsListView

# /warnings
urlpatterns = [
    path('', WarningsListView.as_view(), name='warnings'),
]