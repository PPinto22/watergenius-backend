from django.urls import path

from . import views

# /spaces
urlpatterns = [
    path('', views.spaces, name='spaces'),
    path('/<int:spaceid>', views.space, name='space'), # FIXME - Definir esta view
    path('/<int:spaceid>/restritions/<int:resid>', views.spacesRes, name='spacesRes'),

    #path('restritions/', views.spacesRes, name='spaces'),
    #re_path('(?P<propid>\w+)/managers/(?P<managerid>\w{1,50}[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/
]