from django.urls import path

from api.views.spaces import spaces, spacesRes

# /spaces
urlpatterns = [
    path('', spaces, name='spaces'),
    path('<int:spaceid>/', spaces, name='space'), # TODO - Funcao separada?
    path('<int:spaceid>/restritions/<int:resid>/', spacesRes, name='spacesRes'),
]
