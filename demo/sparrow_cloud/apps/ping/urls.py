# -*- coding: utf-8 -*-


from django.urls import path, re_path
# from . import views
from . import views


urlpatterns = [
    path('xx/', views.ping, name="ping"),
    re_path(r'^re_path/(?P<username>\w+)/$', views.ping, name="ping"),
]
