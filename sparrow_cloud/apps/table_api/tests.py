import os


def setup_settings(settings):
    settings.XX = "1"
    settings.SECRET_KEY = "ss"
    settings.ROOT_URLCONF = 'sparrow_cloud.apps.table_api.urls'


os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"
from django.conf import settings
import django
setup_settings(settings)
django.setup()


from rest_framework import reverse
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import RequestsClient


class TestTableAPI(APITestCase):
    # import pdb; pdb.set_trace()
    # fixtures = [
    #     "tests/fixtures/test_db_data/test_table_data.yaml",
    # ]

    def test_table_api(self):
        import pdb;pdb.set_trace()
        # data = {
        #     "app_lable": "demo",
        #     "model": "testtable",
        #     "filter_condition": {"id": "74101"}
        # }
        import pdb;pdb.set_trace()
        url = reverse('table_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, '')