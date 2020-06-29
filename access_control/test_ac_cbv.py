from collections import OrderedDict

import os
import pytest
from django.conf.urls import include, url
from django.db import models
from django.test import TestCase, override_settings
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import SimpleRouter
from rest_framework.test import APIRequestFactory
from rest_framework.viewsets import GenericViewSet


from sparrow_cloud.access_control.decorators import access_control_cbv_all, access_control_cbv_method
from unittest import mock


class Action(models.Model):
    pass

# ############## 测试 access_control_cbv_all ###############


@access_control_cbv_all("SparrowAdmin")
class CBVAllActionViewSet(GenericViewSet):
    queryset = Action.objects.all()

    def list(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        response = Response()
        response.view = self
        return response

    def retrieve(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        response = Response({"message": "ok"})
        response.view = self
        return response

    def create(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        response = Response({"message": "ok"})
        response.view = self
        return response

    def update(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        response = Response({"message": "ok"})
        response.view = self
        return response

    def destroy(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        response = Response({"message": "ok"})
        response.view = self
        return response

    def partial_update(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        response = Response({"message": "ok"})
        response.view = self
        return response




router = SimpleRouter()
router.register(r'actions', CBVAllActionViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls)),
]


class CBVAllViewSetsTestCase(TestCase):

    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', 
        return_value={"has_perm": False})
    def test_viewset_access_control_cbv_all(self, rest_client_get):
        view = CBVAllActionViewSet.as_view(actions={
            'get': 'list', 
            'post': 'create',
            'delete': 'destroy',
            'put': 'partial_update',
        })
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        # get
        response = view(factory.get('/'))
        assert response.status_code == status.HTTP_403_FORBIDDEN
        # post
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        response = view(factory.post('/1/'))
        assert response.status_code == status.HTTP_403_FORBIDDEN
        # delete
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        response = view(factory.delete('/1/'))
        assert response.status_code == status.HTTP_403_FORBIDDEN
        # put
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        response = view(factory.put('/1/'))
        assert response.status_code == status.HTTP_403_FORBIDDEN

# ############## 测试 access_control_cbv_method ###############


class CBVAllViewSetsTestCaseSkipAccessControl(TestCase):

    def setUp(self):
        settings.ACCESS_CONTROL = {
            "ACCESS_CONTROL_SERVICE": {
                "SERVICE_ADDRESS": "xxxxx:8001"
            },
            "VERIFY_API_PATH": "/verify/",
            # True：跳过， false：不跳过
            "SKIP_ACCESS_CONTROL": os.environ.get("SKIP_ACCESS_CONTROL", True)
        }

    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get',
        return_value={"has_perm": False})
    def test_viewset_access_control_cbv_all(self, rest_client_get):
        view = CBVAllActionViewSet.as_view(actions={
            'get': 'list',
            'post': 'create',
            'delete': 'destroy',
            'put': 'partial_update',
        })
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        # get
        response = view(factory.get('/'))
        assert response.status_code == status.HTTP_200_OK
        # post
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        response = view(factory.post('/1/'))
        assert response.status_code == status.HTTP_200_OK
        # delete
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        response = view(factory.delete('/1/'))
        assert response.status_code == status.HTTP_200_OK
        # put
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        response = view(factory.put('/1/'))
        assert response.status_code == status.HTTP_200_OK

    def tearDown(self):
        settings.ACCESS_CONTROL = {
            "ACCESS_CONTROL_SERVICE": {
                "SERVICE_ADDRESS": "xxxxx:8001"
            },
            "VERIFY_API_PATH": "/verify/",
            # True：跳过， false：不跳过
            "SKIP_ACCESS_CONTROL": os.environ.get("SKIP_ACCESS_CONTROL", False)
        }

# ############## 测试 跳过access_control_cbv_method ###############


@access_control_cbv_method({
    "get": "AdminGet",
    "post": "AdminPost",
    "delete": "AdminDelete",
    "put": "AdminPut",
})
class CBVMethodActionViewSet(GenericViewSet):
    queryset = Action.objects.all()

    def list(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        response = Response()
        response.view = self
        return response

    def retrieve(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        response = Response({"message": "ok"})
        response.view = self
        return response

    def create(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        response = Response({"message": "ok"})
        response.view = self
        return response

    def update(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        response = Response({"message": "ok"})
        response.view = self
        return response

    def destroy(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        response = Response({"message": "ok"})
        response.view = self
        return response

    def partial_update(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        response = Response({"message": "ok"})
        response.view = self
        return response




router.register(r'actions_method', CBVMethodActionViewSet)

urlpatterns = urlpatterns + [
    url(r'^api_cbv_method/', include(router.urls)),
]


class CBVMethodViewSetsTestCase(TestCase):

    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', 
        return_value={"has_perm": False})
    def test_viewset_access_control_cbv_method_get_403(self, rest_client_get):
        view = CBVMethodActionViewSet.as_view(actions={
            'get': 'list', 
            'post': 'create',
            'delete': 'destroy',
            'put': 'partial_update',
        })
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        # get
        response = view(factory.get('/'))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', 
        return_value={"has_perm": True})
    def test_viewset_access_control_cbv_method_get_200(self, rest_client_get):
        view = CBVMethodActionViewSet.as_view(actions={
            'get': 'list', 
            'post': 'create',
            'delete': 'destroy',
            'put': 'partial_update',
        })
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        # get
        response = view(factory.get('/'))
        assert response.status_code == status.HTTP_200_OK


    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', 
        return_value={"has_perm": True})
    def test_viewset_access_control_cbv_method_post_200(self, rest_client_get):
        view = CBVMethodActionViewSet.as_view(actions={
            'get': 'list', 
            'post': 'create',
            'delete': 'destroy',
            'put': 'partial_update',
        })
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        # get
        response = view(factory.post('/'))
        assert response.status_code == status.HTTP_200_OK

    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', 
        return_value={"has_perm": False})
    def test_viewset_access_control_cbv_method_post_403(self, rest_client_get):
        view = CBVMethodActionViewSet.as_view(actions={
            'get': 'list', 
            'post': 'create',
            'delete': 'destroy',
            'put': 'partial_update',
        })
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        # get
        response = view(factory.post('/'))
        assert response.status_code == status.HTTP_403_FORBIDDEN


    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', 
        return_value={"has_perm": True})
    def test_viewset_access_control_cbv_method_delete_200(self, rest_client_get):
        view = CBVMethodActionViewSet.as_view(actions={
            'get': 'list', 
            'post': 'create',
            'delete': 'destroy',
            'put': 'partial_update',
        })
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        # get
        response = view(factory.post('/'))
        assert response.status_code == status.HTTP_200_OK


    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', 
        return_value={"has_perm": False})
    def test_viewset_access_control_cbv_method_delete_403(self, rest_client_get):
        view = CBVMethodActionViewSet.as_view(actions={
            'get': 'list', 
            'post': 'create',
            'delete': 'destroy',
            'put': 'partial_update',
        })
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        # get
        response = view(factory.post('/'))
        assert response.status_code == status.HTTP_403_FORBIDDEN


    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', 
        return_value={"has_perm": True})
    def test_viewset_access_control_cbv_method_put_200(self, rest_client_get):
        view = CBVMethodActionViewSet.as_view(actions={
            'get': 'list', 
            'post': 'create',
            'delete': 'destroy',
            'put': 'partial_update',
        })
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        # get
        response = view(factory.put('/'))
        assert response.status_code == status.HTTP_200_OK


    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get', 
        return_value={"has_perm": False})
    def test_viewset_access_control_cbv_method_put_403(self, rest_client_get):
        view = CBVMethodActionViewSet.as_view(actions={
            'get': 'list', 
            'post': 'create',
            'delete': 'destroy',
            'put': 'partial_update',
        })
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        # get
        response = view(factory.put('/'))
        assert response.status_code == status.HTTP_403_FORBIDDEN


class CBVMethodViewSetsTestCaseSkipAccessControl(TestCase):

    def setUp(self):
        settings.ACCESS_CONTROL = {
            "ACCESS_CONTROL_SERVICE": {
                "SERVICE_ADDRESS": "xxxxx:8001"
            },
            "VERIFY_API_PATH": "/verify/",
            # True：跳过， false：不跳过
            "SKIP_ACCESS_CONTROL": os.environ.get("SKIP_ACCESS_CONTROL", True)
        }

    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get',
        return_value={"has_perm": False})
    def test_viewset_access_control_cbv_method_get_403(self, rest_client_get):
        view = CBVMethodActionViewSet.as_view(actions={
            'get': 'list',
            'post': 'create',
            'delete': 'destroy',
            'put': 'partial_update',
        })
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        # get
        response = view(factory.get('/'))
        assert response.status_code == status.HTTP_200_OK

    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get',
        return_value={"has_perm": True})
    def test_viewset_access_control_cbv_method_get_200(self, rest_client_get):
        view = CBVMethodActionViewSet.as_view(actions={
            'get': 'list',
            'post': 'create',
            'delete': 'destroy',
            'put': 'partial_update',
        })
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        # get
        response = view(factory.get('/'))
        assert response.status_code == status.HTTP_200_OK


    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get',
        return_value={"has_perm": True})
    def test_viewset_access_control_cbv_method_post_200(self, rest_client_get):
        view = CBVMethodActionViewSet.as_view(actions={
            'get': 'list',
            'post': 'create',
            'delete': 'destroy',
            'put': 'partial_update',
        })
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        # get
        response = view(factory.post('/'))
        assert response.status_code == status.HTTP_200_OK

    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get',
        return_value={"has_perm": False})
    def test_viewset_access_control_cbv_method_post_403(self, rest_client_get):
        view = CBVMethodActionViewSet.as_view(actions={
            'get': 'list',
            'post': 'create',
            'delete': 'destroy',
            'put': 'partial_update',
        })
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        # get
        response = view(factory.post('/'))
        assert response.status_code == status.HTTP_200_OK


    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get',
        return_value={"has_perm": True})
    def test_viewset_access_control_cbv_method_delete_200(self, rest_client_get):
        view = CBVMethodActionViewSet.as_view(actions={
            'get': 'list',
            'post': 'create',
            'delete': 'destroy',
            'put': 'partial_update',
        })
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        # get
        response = view(factory.post('/'))
        assert response.status_code == status.HTTP_200_OK


    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get',
        return_value={"has_perm": False})
    def test_viewset_access_control_cbv_method_delete_403(self, rest_client_get):
        view = CBVMethodActionViewSet.as_view(actions={
            'get': 'list',
            'post': 'create',
            'delete': 'destroy',
            'put': 'partial_update',
        })
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        # get
        response = view(factory.post('/'))
        assert response.status_code == status.HTTP_200_OK


    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get',
        return_value={"has_perm": True})
    def test_viewset_access_control_cbv_method_put_200(self, rest_client_get):
        view = CBVMethodActionViewSet.as_view(actions={
            'get': 'list',
            'post': 'create',
            'delete': 'destroy',
            'put': 'partial_update',
        })
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        # get
        response = view(factory.put('/'))
        assert response.status_code == status.HTTP_200_OK


    @mock.patch('sparrow_cloud.access_control.access_verify.rest_client.get',
        return_value={"has_perm": False})
    def test_viewset_access_control_cbv_method_put_403(self, rest_client_get):
        view = CBVMethodActionViewSet.as_view(actions={
            'get': 'list',
            'post': 'create',
            'delete': 'destroy',
            'put': 'partial_update',
        })
        factory = APIRequestFactory(REMOTE_USER='sssssssss')
        # get
        response = view(factory.put('/'))
        assert response.status_code == status.HTTP_200_OK

    def tearDown(self):
        settings.ACCESS_CONTROL = {
            "ACCESS_CONTROL_SERVICE": {
                "SERVICE_ADDRESS": "xxxxx:8001"
            },
            "VERIFY_API_PATH": "/verify/",
            # True：跳过， false：不跳过
            "SKIP_ACCESS_CONTROL": os.environ.get("SKIP_ACCESS_CONTROL", False)
        }