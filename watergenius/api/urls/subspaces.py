from django.urls import path

from api.views.subspaces import subspaces

# /subspaces
urlpatterns = [
    path('', subspaces, name='subspaces'),
    path('<int:subspaceid>/', subspaces, name='subspace'), # TODO - funcao separada?
]