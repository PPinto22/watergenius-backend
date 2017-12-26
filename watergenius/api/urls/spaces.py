from django.urls import path

from api.views.spaces import spaces, spacesRes

# /spaces
urlpatterns = [
    path('', spaces, name='spaces'),
    # path('<int:spaceid>/', views.space, name='space'),  TODO - Definir esta view
    path('<int:spaceid>/restritions/<int:resid>/', spacesRes, name='spacesRes'),
]
