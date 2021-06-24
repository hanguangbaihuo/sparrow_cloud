import json
import os
from django.conf.urls import include, url
from django.db import models
from django.test import TestCase, override_settings
from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework.viewsets import GenericViewSet
from unittest import mock

X_JWT_PAYLOAD=json.dumps({'uid': '1234abc', 'exp': 1722200316, 'iat': 1622193116, 'app_id': 'app_1234567'})

class CBVAllViewSetsTestCase(TestCase):
    '''
    测试类视图装饰器 access_control_cbv_all
    '''
    @classmethod
    def setUpClass(cls):
        settings.SPARROW_AUTHENTICATION = {"USER_CLASS_PATH": "sparrow_cloud.auth.user.User"}
        # settings.SC_SKIP_ACCESS_CONTROL = False
        os.environ.setdefault("SC_ACCESS_CONTROL_SVC","ac-svc:8001")
        os.environ.setdefault("SC_ACCESS_CONTROL_API","/api/ac")

    @classmethod
    def tearDownClass(cls):
        pass


    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', return_value={"has_perm": False})
    def test_access_control_cbv_all_no_perm(self, rest_client_get):
        # 不跳过访问控制，没权限访问
        settings.SC_SKIP_ACCESS_CONTROL = False
        from sparrow_cloud.access_control.decorators import access_control_cbv_all

        class Action(models.Model):
            pass

        @access_control_cbv_all("SparrowAdmin")
        class CBVAllActionViewSet(GenericViewSet):
            queryset = Action.objects.all()

            def list(self, request, *args, **kwargs):
                # import pdb; pdb.set_trace()
                response = Response()
                response.view = self
                return response

        view = CBVAllActionViewSet.as_view(actions={
            'get': 'list',
        })
        
        factory = APIRequestFactory(HTTP_X_JWT_PAYLOAD=X_JWT_PAYLOAD)
        response = view(factory.get('/'))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', return_value={"has_perm": True})
    def test_access_control_cbv_all_allow(self, rest_client_get):
        # 不跳过访问控制，有权限访问
        settings.SC_SKIP_ACCESS_CONTROL = False
        from sparrow_cloud.access_control.decorators import access_control_cbv_all

        class Action(models.Model):
            pass

        @access_control_cbv_all("SparrowAdmin")
        class CBVAllActionViewSet(GenericViewSet):
            queryset = Action.objects.all()

            def list(self, request, *args, **kwargs):
                response = Response()
                response.view = self
                return response

        view = CBVAllActionViewSet.as_view(actions={
            'get': 'list',
        })
        
        factory = APIRequestFactory(HTTP_X_JWT_PAYLOAD=X_JWT_PAYLOAD)
        response = view(factory.get('/'))
        assert response.status_code == status.HTTP_200_OK

    # @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', return_value={"has_perm": False})
    def test_viewset_access_control_cbv_all_skip_ac(self):
        # 跳过访问控制，没有mock远程，也没有认证
        settings.SC_SKIP_ACCESS_CONTROL = True
        from sparrow_cloud.access_control.decorators import access_control_cbv_all

        class Action(models.Model):
            pass

        @access_control_cbv_all("SparrowAdmin")
        class CBVAllActionViewSet(GenericViewSet):
            queryset = Action.objects.all()

            def list(self, request, *args, **kwargs):
                # import pdb; pdb.set_trace()
                response = Response()
                response.view = self
                return response

        view = CBVAllActionViewSet.as_view(actions={
            'get': 'list',
        })
        
        factory = APIRequestFactory()# 无认证，HTTP_X_JWT_PAYLOAD=X_JWT_PAYLOAD
        response = view(factory.get('/'))
        assert response.status_code == status.HTTP_200_OK


class CBVMethodViewSetsTestCase(TestCase):
    '''
    测试类视图装饰器 access_control_cbv_method
    '''
    @classmethod
    def setUpClass(cls):
        settings.SPARROW_AUTHENTICATION = {"USER_CLASS_PATH": "sparrow_cloud.auth.user.User"}
        # settings.SC_SKIP_ACCESS_CONTROL = False
        os.environ.setdefault("SC_ACCESS_CONTROL_SVC","ac-svc:8001")
        os.environ.setdefault("SC_ACCESS_CONTROL_API","/api/ac")

    @classmethod
    def tearDownClass(cls):
        pass


    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', return_value={"has_perm": False})
    def test_viewset_access_control_cbv_method(self, rest_client_mock):
        # 不跳过访问控制，无权限访问
        settings.SC_SKIP_ACCESS_CONTROL = False
        from sparrow_cloud.access_control.decorators import access_control_cbv_method

        class Action(models.Model):
            pass

        @access_control_cbv_method({
            "get": "AdminGet",
            "post": "AdminPost",
            "delete": "AdminDelete",
            "put": "AdminPut",
        })
        class CBVAllActionViewSet(GenericViewSet):
            queryset = Action.objects.all()

            def list(self, request, *args, **kwargs):
                response = Response()
                response.view = self
                return response
            def create(self, request, *args, **kwargs):
                response = Response({"message": "ok"})
                response.view = self
                return response
            def destroy(self, request, *args, **kwargs):
                response = Response({"message": "ok"})
                response.view = self
                return response
            def partial_update(self, request, *args, **kwargs):
                response = Response({"message": "ok"})
                response.view = self
                return response

        view = CBVAllActionViewSet.as_view(actions={
                'get': 'list', 
                'post': 'create',
                'delete': 'destroy',
                'put': 'partial_update',
            })
        
        factory = APIRequestFactory(HTTP_X_JWT_PAYLOAD=X_JWT_PAYLOAD)
        response = view(factory.get('/'))
        assert response.status_code == status.HTTP_403_FORBIDDEN
        response = view(factory.post('/'))
        assert response.status_code == status.HTTP_403_FORBIDDEN
        response = view(factory.delete('/'))
        assert response.status_code == status.HTTP_403_FORBIDDEN
        response = view(factory.put('/'))
        assert response.status_code == status.HTTP_403_FORBIDDEN


    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', return_value={"has_perm": True})
    def test_access_control_cbv_method_allow(self, rest_client_mock):
        # 不跳过访问控制，有权限访问
        settings.SC_SKIP_ACCESS_CONTROL = False
        from sparrow_cloud.access_control.decorators import access_control_cbv_method

        class Action(models.Model):
            pass

        @access_control_cbv_method({
            "get": "AdminGet",
            "post": "AdminPost",
            "delete": "AdminDelete",
            "put": "AdminPut",
        })
        class CBVAllActionViewSet(GenericViewSet):
            queryset = Action.objects.all()

            def list(self, request, *args, **kwargs):
                response = Response()
                response.view = self
                return response
            def create(self, request, *args, **kwargs):
                response = Response({"message": "ok"})
                response.view = self
                return response
            def destroy(self, request, *args, **kwargs):
                response = Response({"message": "ok"})
                response.view = self
                return response
            def partial_update(self, request, *args, **kwargs):
                response = Response({"message": "ok"})
                response.view = self
                return response

        view = CBVAllActionViewSet.as_view(actions={
                'get': 'list', 
                'post': 'create',
                'delete': 'destroy',
                'put': 'partial_update',
            })
        
        factory = APIRequestFactory(HTTP_X_JWT_PAYLOAD=X_JWT_PAYLOAD)
        response = view(factory.get('/'))
        assert response.status_code == status.HTTP_200_OK
        response = view(factory.post('/'))
        assert response.status_code == status.HTTP_200_OK
        response = view(factory.delete('/'))
        assert response.status_code == status.HTTP_200_OK
        response = view(factory.put('/'))
        assert response.status_code == status.HTTP_200_OK

    # @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', return_value={"has_perm": False})
    def test_viewset_access_control_cbv_method_skip_ac(self):
        # 跳过访问控制，没有mock远程，也没有认证
        settings.SC_SKIP_ACCESS_CONTROL = True
        from sparrow_cloud.access_control.decorators import access_control_cbv_method

        class Action(models.Model):
            pass

        @access_control_cbv_method({
            "get": "AdminGet",
            "post": "AdminPost",
            "delete": "AdminDelete",
            "put": "AdminPut",
        })
        class CBVAllActionViewSet(GenericViewSet):
            queryset = Action.objects.all()

            def list(self, request, *args, **kwargs):
                response = Response()
                response.view = self
                return response
            def create(self, request, *args, **kwargs):
                response = Response({"message": "ok"})
                response.view = self
                return response
            def destroy(self, request, *args, **kwargs):
                response = Response({"message": "ok"})
                response.view = self
                return response
            def partial_update(self, request, *args, **kwargs):
                response = Response({"message": "ok"})
                response.view = self
                return response

        view = CBVAllActionViewSet.as_view(actions={
                'get': 'list', 
                'post': 'create',
                'delete': 'destroy',
                'put': 'partial_update',
            })
        
        factory = APIRequestFactory()
        response = view(factory.get('/'))
        assert response.status_code == status.HTTP_200_OK
        response = view(factory.post('/'))
        assert response.status_code == status.HTTP_200_OK
        response = view(factory.delete('/'))
        assert response.status_code == status.HTTP_200_OK
        response = view(factory.put('/'))
        assert response.status_code == status.HTTP_200_OK