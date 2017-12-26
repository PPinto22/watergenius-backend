from django.urls import include, path, re_path

from api.views.users import UserView, userByMail

# /users
urlpatterns = [
    # Register and authentication paths are defined on api.urls

    path('', UserView.as_view()),
    re_path(r'^(?P<mail>\w{1,50}[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', userByMail),
]