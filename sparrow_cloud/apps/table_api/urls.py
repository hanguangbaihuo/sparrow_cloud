from django.conf.urls import url
from . import views


urlpatterns = [
    url('', views.TableView.as_view(), name="table_api"),
]