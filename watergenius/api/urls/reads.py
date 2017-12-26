from django.urls import path

from api.views.reads import reads

# /reads
urlpatterns = [
    path('', reads, name='reads'),
    path('<int:readid>/', reads, name='read'),  # TODO - funcao separada?
]