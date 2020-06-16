import pytest
from django.test import TestCase

from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import (
    action, api_view, authentication_classes, parser_classes,
    permission_classes, renderer_classes, schema, throttle_classes
)
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.test import APIRequestFactory
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from django.conf import settings
import os


####### 我们的import ########

from sparrow_cloud.access_control.decorators import access_control_fbv
from unittest import mock



class DecoratorTestCase(TestCase):


    def setUp(self):
        # self.factory = APIRequestFactory("REMOTE_USER")
        pass

    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', 
        return_value={"has_perm": False})
    def test_calling_method_403(self, rest_client_get):
        self.factory = APIRequestFactory(REMOTE_USER='sssssssss')
        
        # 测试有权限
        @api_view(['GET'])
        @access_control_fbv("SparrowAdmin")
        def view(request):
            return Response({})

        request = self.factory.get('/')
        response = view(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', 
    return_value={"has_perm": True})
    def test_calling_method(self, rest_client_get):
        self.factory = APIRequestFactory(REMOTE_USER='sssssssss')
        
        # 测试有权限
        @api_view(['GET'])
        @access_control_fbv("SparrowAdmin")
        def view(request):
            return Response({})

        request = self.factory.get('/')
        response = view(request)
        assert response.status_code == status.HTTP_200_OK



class DecoratorTestCaseSkipAccessControl(TestCase):

    def setUp(self):
        settings.ACCESS_CONTROL = {
            "ACCESS_CONTROL_SERVICE": {
                "ENV_NAME": "SPARROW_ACCESS_CONTROL",
                "VALUE": os.environ.get("SPARROW_ACCESS_CONTROL", "xxxxx"),
            },
            "VERIFY_API_PATH": "/verify/",
            # True：跳过， false：不跳过
            "SKIP_ACCESS_CONTROL": os.environ.get("SKIP_ACCESS_CONTROL", True)
        }

    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get',
                return_value={"has_perm": False})
    def test_calling_method_403_skip(self, rest_client_get):
        self.factory = APIRequestFactory(REMOTE_USER='sssssssss')

        # 测试有权限
        @api_view(['GET'])
        @access_control_fbv("SparrowAdmin")
        def view(request):
            return Response({})

        request = self.factory.get('/')
        response = view(request)
        assert response.status_code == status.HTTP_200_OK

    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get',
                return_value={"has_perm": True})
    def test_calling_method_skip(self, rest_client_get):
        self.factory = APIRequestFactory(REMOTE_USER='sssssssss')

        # 测试有权限
        @api_view(['GET'])
        @access_control_fbv("SparrowAdmin")
        def view(request):
            return Response({})

        request = self.factory.get('/')
        response = view(request)
        assert response.status_code == status.HTTP_200_OK

    def tearDown(self):
        settings.ACCESS_CONTROL = {
            "ACCESS_CONTROL_SERVICE": {
                "ENV_NAME": "SPARROW_ACCESS_CONTROL",
                "VALUE": os.environ.get("SPARROW_ACCESS_CONTROL", "xxxxx"),
            },
            "VERIFY_API_PATH": "/verify/",
            # True：跳过， false：不跳过
            "SKIP_ACCESS_CONTROL": os.environ.get("SKIP_ACCESS_CONTROL", False)
        }