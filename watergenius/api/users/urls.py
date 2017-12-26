from django.urls import include, path, re_path

from . import views

# Path: /users
urlpatterns = [
    # Register and authentication paths are defined on api.urls

    path('', views.UserView.as_view()),
    # re_path('/(?P<mail>\w{1,50}[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/', userByMail),
]