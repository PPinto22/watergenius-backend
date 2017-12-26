from django.urls import path

from api.views.embeddedsys import embeddedsystems

# /embeddedsys
urlpatterns = [
    path('', embeddedsystems, name='embeddedsystems'),
    path('<int:sysid>/', embeddedsystems, name='embeddedsystem'),  # TODO - funcao separada?
]