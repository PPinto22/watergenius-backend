from django.urls import path

from api.views.embeddedsys import EmbeddedSysListView, EmbeddedSysDetailView

# /embeddedsys
urlpatterns = [
    path('', EmbeddedSysListView, name='embeddedsystems'),
    path('<int:sysid>/', EmbeddedSysDetailView, name='embeddedsystem'),
]