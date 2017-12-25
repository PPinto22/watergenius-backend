from django.urls import path ,register_converter, re_path
from . import views, converters


#register_converter(converters.MailConverter, 'mail')

urlpatterns = [
    #new in django 2.0
    #re_path('(?P<mail>\w{1,50}[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/', views.usersMail, ),
    #  path('', views.usersMail, name='usersMail'),
    #path('', views.login_view, name='login_view'),
    path('', views.spaces, name='spaces'),
    re_path('(?P<spaceid>\d+)/restritions/(?P<resid>\d+|)',  views.spacesRes, name='spacesRes'),
    #path('restritions/', views.spacesRes, name='spaces'),
    #re_path('(?P<propid>\w+)/managers/(?P<managerid>\w{1,50}[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/


]