from django.urls import path ,register_converter, re_path
from . import views, converters


#register_converter(converters.MailConverter, 'mail')

urlpatterns = [
    #new in django 2.0
    re_path('[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}', views.usersMail, name='usersMail'),
  #  path('', views.usersMail, name='usersMail'),
    path('', views.usersNormal, name='usersNormal'),


]