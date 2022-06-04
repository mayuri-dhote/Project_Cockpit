from os import path
from . import views
from django.urls import re_path as url
from django.urls import path , include
urlpatterns = [
    # path('', views.index, name='index'),
    url(r'^api/getrs$', views.getrs),
    url(r'^api/cert$', views.submit_cert),
]