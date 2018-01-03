from django.urls import path, re_path

from api.views.users import UserListView, UserDetailView

# /users
urlpatterns = [
    path('', UserListView.as_view()),
    re_path(r'^(?P<mail>\w{1,50}[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/', UserDetailView.as_view()),
]