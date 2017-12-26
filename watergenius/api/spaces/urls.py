from django.urls import path

from . import views

# /spaces
urlpatterns = [
    path('', views.spaces, name='spaces'),
    path('/<int:spaceid>', views.space, name='space'),  # FIXME - Definir esta view
    path('/<int:spaceid>/restritions/<int:resid>', views.spacesRes, name='spacesRes'),
]
