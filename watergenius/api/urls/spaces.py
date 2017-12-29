from django.urls import path

from api.views.spaces import spaces, spacesRes

# /spaces
urlpatterns = [
    path('', spaces, name='spaces'),
    path('<int:spaceid>/', spaces, name='spaces'), # TODO - Funcao separada?
    path('<int:spaceid>/restritions/<int:resid>/', spacesRes, name='spacesRes'),
    path('<int:spaceid>/restritions/', spacesRes, name='spacesRes')
]
