from django.urls import path

from api.views.reads import ReadsListView, ReadDetailView

# /reads
urlpatterns = [
    path('', ReadsListView.as_view(), name='reads'),
    path('<int:readid>/', ReadDetailView.as_view(), name='read'),
]