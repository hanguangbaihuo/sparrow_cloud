from django.urls import path
from . import views


urlpatterns = [
    path('', views.TableView.as_view(), name="table_api"),
]