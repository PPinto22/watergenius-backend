from django.urls import path

from api.views.embeddedsys import EmbeddedSysListView, EmbeddedSysDetailView

# /embeddedsys
urlpatterns = [
    path('', EmbeddedSysListView.as_view(), name='embeddedsystems'),
    path('<int:sysid>/', EmbeddedSysDetailView.as_view(), name='embeddedsystem'),
]