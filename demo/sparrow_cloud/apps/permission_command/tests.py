from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
import sys
import logging


logger = logging.getLogger(__name__)

class AllUrlTests(APITestCase):
    #url(r'^cachetest_detail/$', views.cachetest_detail, name="cachetest_detail_view"), 
    def test_010_cachetest_detail_view(self):
        url = reverse("cachetest_detail_view")
        logger.info('....................url = {0}'.format(url))
        response = self.client.get(url)
        fun_name = sys._getframe().f_code.co_name
        print("fun_name = ", fun_name)
        print("response.status_code = ",response.status_code)
        print("response = ",response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'CacheTest001')