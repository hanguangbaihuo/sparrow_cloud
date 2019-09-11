from django.urls import path
from . import views


urlpatterns = [
    path('', views.table_api, name="table_api"),
]