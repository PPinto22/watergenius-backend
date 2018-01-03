from django.urls import path

from api.views.spaces import SpacesListView, SpaceDetailView, SpaceRestrictionsListView, \
    SpaceRestrictionDetailView

# /spaces
urlpatterns = [
    path('', SpacesListView.as_view(), name='spaces'),
    path('<int:spaceid>/', SpaceDetailView.as_view(), name='spaceDetail'),
    path('<int:spaceid>/restritions/', SpaceRestrictionsListView.as_view(), name='spaceRestrictions'),
    path('<int:spaceid>/restritions/<int:resid>/', SpaceRestrictionDetailView.as_view(), name='spaceRestriction'),
]

