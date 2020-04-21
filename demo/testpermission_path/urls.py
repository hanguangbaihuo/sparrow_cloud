"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from . import views
# from rest_framework.routers import DefaultRouter

urlpatterns = [
    re_path(r'^xx/(?P<username>\w+)/$', views.test_path_params_1, name="test_path_params_1"),
    re_path(r'^(?P<id>\w+)/yy/(?P<username>\w+)/$', views.test_path_params_2, name="test_path_params_2"),
    path(r'yy/zz/', views.test_path_no_params_2, name="test_path_no_params_2"),
    path(r'mm/', views.test_path_no_params_1, name="test_path_no_params_1"),
]
