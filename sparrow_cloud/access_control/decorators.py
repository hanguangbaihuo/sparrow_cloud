import json
import logging

from functools import wraps

from django.conf import settings
from django.http import HttpResponse
from django.utils.decorators import method_decorator

from sparrow_cloud.access_control.access_verify import access_verify
from sparrow_cloud.utils.get_settings_value import get_settings_value, get_service_name

logger = logging.getLogger(__name__)

DETAIL_403 = {"message": "无权限访问。", "code":233403}
DETAIL_401 = {"message": "身份认证信息未提供。","code":233401}


def access_control_fbv(resource=None):
    """FBV
        resource: "example_admin"
        configmap ：
            SC_ACCESS_CONTROL_SVC
            SC_ACCESS_CONTROL_API
    """
    def decorator(func):
        @wraps(func)
        def wrap(request, *args, **kwargs):
            skip_access_control = getattr(settings, "SC_SKIP_ACCESS_CONTROL", False)
            if skip_access_control is False or skip_access_control == 'False':
                user_id = request.META["REMOTE_USER"]
                if user_id is None:
                    return HttpResponse(json.dumps(DETAIL_401), content_type='application/json; charset=utf-8', status=401)
                app_name = get_service_name()
                if not access_verify(user_id=user_id, app_name=app_name, resource_code=resource):
                    return HttpResponse(json.dumps(DETAIL_403), content_type='application/json; charset=utf-8', status=403)
                return func(request, *args, **kwargs)
            return func(request, *args, **kwargs)
        return wrap
    return decorator


def access_control_cbv_all(resource=None):
    """all
        resource: "example_admin"
        configmap：
            SC_ACCESS_CONTROL_SVC
            SC_ACCESS_CONTROL_API
    """
    def decorator(view):
        def func(function):
            def wrap(request, *args, **kwargs):
                skip_access_control = getattr(settings, "SC_SKIP_ACCESS_CONTROL", False)
                if skip_access_control is False or skip_access_control == 'False':
                    user_id = request.META["REMOTE_USER"]
                    if user_id is None:
                        return HttpResponse(json.dumps(DETAIL_401), content_type='application/json; charset=utf-8', status=401)
                    app_name = get_service_name()
                    if not access_verify(user_id=user_id, app_name=app_name, resource_code=resource):
                        return HttpResponse(json.dumps(DETAIL_403), content_type='application/json; charset=utf-8', status=403)
                    return function(request, *args, **kwargs)
                return function(request, *args, **kwargs)
            return wrap
        view.dispatch = method_decorator(func)(view.dispatch)
        return view
    return decorator


def access_control_cbv_method(resource):
    """method
        resource: {
                "get": "example1_admin",
                "post": "example1_admin1"
              }
        configmap：
            SC_ACCESS_CONTROL_SVC
            SC_ACCESS_CONTROL_API
    """
    def decorator(view):
        def func(function):
            def wrap(request, *args, **kwargs):
                skip_access_control = getattr(settings, "SC_SKIP_ACCESS_CONTROL", False)
                if skip_access_control is False or skip_access_control == 'False':
                    user_id = request.META["REMOTE_USER"]
                    app_name = get_service_name()
                    resource_code = (dict((k.lower(), v) for k, v in resource.items())).get(request.method.lower())
                    if resource_code:
                        if user_id is None:
                            return HttpResponse(json.dumps(DETAIL_401), content_type='application/json; charset=utf-8', status=401)
                        if not access_verify(user_id=user_id, app_name=app_name, resource_code=resource_code):
                            return HttpResponse(json.dumps(DETAIL_403), content_type='application/json; charset=utf-8', status=403)
                    return function(request, *args, **kwargs)
                return function(request, *args, **kwargs)
            return wrap
        view.dispatch = method_decorator(func)(view.dispatch)
        return view
    return decorator
