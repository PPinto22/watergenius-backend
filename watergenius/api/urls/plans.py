from django.urls import path

from api.views.plans import PlansListView, PlanDetailView

# /plans
urlpatterns = [
    path('', PlansListView.as_view(), name='plans'),
    path('<int:planid>/', PlanDetailView.as_view(), name='plan'),
]