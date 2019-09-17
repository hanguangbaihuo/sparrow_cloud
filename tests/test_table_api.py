import os
from django.urls import reverse
from django.urls import path, include


def setup_settings(settings):
    settings.XX = "1"
    settings.SECRET_KEY = "ss"
    settings.ROOT_URLCONF = __name__


os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"

import django
from django.conf import settings
from rest_framework.test import APITestCase


setup_settings(settings)
django.setup()

urlpatterns = [
        path("api/", include("sparrow_cloud.apps.table_api.urls"))
    ]


class TestTableAPI(APITestCase):

    def setUp(self):
        setup_settings(settings)
        django.setup()

    def test_table_api_no_parameter(self):
        """无参数"""
        url = reverse('table_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'code': 1, 'message': '参数不全，请检查参数：app_lable/model/filter_condition'})

    # def test_table_api_bad_parameter(self):
    #     """错误参数"""
    #     filter_data = {
    #         "app_lable": "table_api",
    #         "model": "TestTable",
    #         "filter_condition": {"brand_num": "1", "name": "lisi"}
    #     }
    #     url = reverse('table_api')
    #     response = self.client.get(path=url, data=filter_data)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.json(), {'code': 1, 'message': "App 'table_api' doesn't have a 'table_api' model."})
