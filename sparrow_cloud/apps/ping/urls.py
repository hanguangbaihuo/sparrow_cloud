# -*- coding: utf-8 -*-


from django.urls import path, re_path
# from . import views
from . import views


urlpatterns = [
    path('', views.ping, name="ping"),
]
