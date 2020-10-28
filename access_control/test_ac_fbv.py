from django.test import TestCase

from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from django.conf import settings
import os


####### 我们的import ########

from sparrow_cloud.access_control.decorators import access_control_fbv
from unittest import mock


class DecoratorTestCase(TestCase):

    def setUp(self):
        settings.SC_SKIP_ACCESS_CONTROL = False

    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', return_value={"has_perm": False})
    def test_calling_method_403_fbc(self, rest_client_get):
        self.factory = APIRequestFactory(REMOTE_USER='sssssssss')
        
        # 测试有权限
        @api_view(['GET'])
        @access_control_fbv("SparrowAdmin")
        def view(request):
            return Response({})

        request = self.factory.get('/')
        response = view(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', return_value={"has_perm": True})
    def test_calling_method_fbv(self, rest_client_get):
        self.factory = APIRequestFactory(REMOTE_USER='sssssssss')
        
        # 测试有权限
        @api_view(['GET'])
        @access_control_fbv("SparrowAdmin")
        def view(request):
            return Response({})

        request = self.factory.get('/')
        response = view(request)
        assert response.status_code == status.HTTP_200_OK

    def test_calling_method_401_fbv(self):
        self.factory = APIRequestFactory(REMOTE_USER=None)
        # 测试无用户
        @api_view(['GET'])
        @access_control_fbv("SparrowAdmin")
        def view(request):
            return Response({})

        request = self.factory.get('/')

        response = view(request)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class DecoratorTestCaseSkipAccessControl(TestCase):

    def setUp(self):
        settings.SC_SKIP_ACCESS_CONTROL = True

    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', return_value={"has_perm": False})
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

    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', return_value={"has_perm": True})
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

    def test_calling_method_401_skip(self):
        self.factory = APIRequestFactory(REMOTE_USER=None)

        # 测试有权限
        @api_view(['GET'])
        @access_control_fbv("SparrowAdmin")
        def view(request):
            return Response({})
        request = self.factory.get('/')
        response = view(request)
        assert response.status_code == status.HTTP_200_OK

    def tearDown(self):
        settings.SC_SKIP_ACCESS_CONTROL = False