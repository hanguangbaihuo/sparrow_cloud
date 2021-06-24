from django.test import TestCase
import json
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from django.conf import settings
import os
from unittest import mock

X_JWT_PAYLOAD=json.dumps({'uid': '1234abc', 'exp': 1722200316, 'iat': 1622193116, 'app_id': 'app_1234567'})

class DecoratorTestCase(TestCase):
    '''
    测试不跳过访问控制情况下，方法类装饰器
    '''
    @classmethod
    def setUpClass(cls):
        settings.SPARROW_AUTHENTICATION = {"USER_CLASS_PATH": "sparrow_cloud.auth.user.User"}
        settings.SC_SKIP_ACCESS_CONTROL = False
        os.environ.setdefault("SC_ACCESS_CONTROL_SVC","ac-svc:8001")
        os.environ.setdefault("SC_ACCESS_CONTROL_API","/api/ac")
    
    @classmethod
    def tearDownClass(cls):
        pass

    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', return_value={"has_perm": False})
    def test_calling_method_403_fbc(self, rest_client_get):
        '''
        无权限
        '''
        from sparrow_cloud.access_control.decorators import access_control_fbv
        @api_view(['GET'])
        @access_control_fbv("SparrowAdmin")
        def view(request):
            return Response({})
        
        self.factory = APIRequestFactory(HTTP_X_JWT_PAYLOAD=X_JWT_PAYLOAD)
        request = self.factory.get('/')
        response = view(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', return_value={"has_perm": True})
    def test_calling_method_fbv(self, rest_client_get):
        '''
        有权限
        '''
        from sparrow_cloud.access_control.decorators import access_control_fbv
        @api_view(['GET'])
        @access_control_fbv("SparrowAdmin")
        def view(request):
            return Response({})

        self.factory = APIRequestFactory(HTTP_X_JWT_PAYLOAD=X_JWT_PAYLOAD)
        request = self.factory.get('/')
        response = view(request)
        assert response.status_code == status.HTTP_200_OK

    def test_calling_method_401_fbv(self):
        '''
        用户未认证
        '''
        from sparrow_cloud.access_control.decorators import access_control_fbv
        @api_view(['GET'])
        @access_control_fbv("SparrowAdmin")
        def view(request):
            return Response({})
        
        self.factory = APIRequestFactory()
        request = self.factory.get('/')
        response = view(request)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class DecoratorTestCaseSkipAccessControl(TestCase):
    '''
    测试设置跳过访问控制，方法装饰器
    '''
    @classmethod
    def setUpClass(cls):
        settings.SPARROW_AUTHENTICATION = {"USER_CLASS_PATH": "sparrow_cloud.auth.user.User"}
        settings.SC_SKIP_ACCESS_CONTROL = True
        os.environ.setdefault("SC_ACCESS_CONTROL_SVC","ac-svc:8001")
        os.environ.setdefault("SC_ACCESS_CONTROL_API","/api/ac")
    
    @classmethod
    def tearDownClass(cls):
        pass

    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', return_value={"has_perm": False})
    def test_calling_method_403_skip(self, rest_client_get):
        from sparrow_cloud.access_control.decorators import access_control_fbv
        @api_view(['GET'])
        @access_control_fbv("SparrowAdmin")
        def view(request):
            return Response({})
        
        self.factory = APIRequestFactory()
        request = self.factory.get('/')
        response = view(request)
        assert response.status_code == status.HTTP_200_OK

    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', return_value={"has_perm": True})
    def test_calling_method_skip(self, rest_client_get):
        from sparrow_cloud.access_control.decorators import access_control_fbv
        @api_view(['GET'])
        @access_control_fbv("SparrowAdmin")
        def view(request):
            return Response({})
        
        self.factory = APIRequestFactory()
        request = self.factory.get('/')
        response = view(request)
        assert response.status_code == status.HTTP_200_OK

    def test_calling_method_401_skip(self):
        from sparrow_cloud.access_control.decorators import access_control_fbv
        @api_view(['GET'])
        @access_control_fbv("SparrowAdmin")
        def view(request):
            return Response({})
        
        self.factory = APIRequestFactory()
        request = self.factory.get('/')
        response = view(request)
        assert response.status_code == status.HTTP_200_OK

#     def tearDown(self):
#         settings.SC_SKIP_ACCESS_CONTROL = False