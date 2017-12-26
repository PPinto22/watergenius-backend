from django.urls import path

from api.views.plans import plans

# /plans
urlpatterns = [
    path('', plans, name='plans'),
    path('<int:planid>/', plans, name='plan'), # TODO - funcao separada?
]