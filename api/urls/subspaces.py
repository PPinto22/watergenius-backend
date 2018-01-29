from django.urls import path

from api.views.subspaces import SubspacesListView, SubspaceDetailView

# /subspaces
urlpatterns = [
    path('', SubspacesListView.as_view(), name='subspaces'),
    path('<int:subspaceid>/', SubspaceDetailView.as_view(), name='subspace'),
]