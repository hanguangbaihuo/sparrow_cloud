import json
import logging

from functools import wraps

from rest_framework.exceptions import PermissionDenied

from django.http import HttpResponse
from django.utils.decorators import method_decorator

from sparrow_cloud.access_control.access_verify import access_verify
from sparrow_cloud.utils.get_settings_value import get_settings_value

logger = logging.getLogger(__name__)

DETAIL = {"detail": "You do not have permission to perform this action."}


def access_control_fbv(resource=None):
    """FBV
        resource: "example_admin"
    """
    def decorator(func):
        @wraps(func)
        def wrap(request, *args, **kwargs):
            user_id = request.META["REMOTE_USER"]
            if user_id is None:
                raise PermissionDenied()
            app_name = get_settings_value("SERVICE_CONF").get("NAME", None)
            if not access_verify(user_id=user_id, app_name=app_name, resource_code=resource):
                raise PermissionDenied()
            return func(request, *args, **kwargs)
        return wrap
    return decorator


def access_control_cbv_all(resource=None):
    """all
        resource: "example_admin"
    """
    def decorator(view):
        def func(function):
            def wrap(request, *args, **kwargs):
                user_id = request.META["REMOTE_USER"]
                if user_id is None:
                    return HttpResponse(json.dumps(DETAIL), content_type='application/json; charset=utf-8', status=403)
                app_name = get_settings_value("SERVICE_CONF").get("NAME", None)
                if not access_verify(user_id=user_id, app_name=app_name, resource_code=resource):
                    return HttpResponse(json.dumps(DETAIL), content_type='application/json; charset=utf-8', status=403)
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
    """
    def decorator(view):
        def func(function):
            def wrap(request, *args, **kwargs):
                user_id = request.META["REMOTE_USER"]
                if user_id is None:
                    raise PermissionDenied()
                resource_code = (dict((k.lower(), v) for k, v in resource.items())).get(request.method.lower())
                if resource_code:
                    app_name = get_settings_value("SERVICE_CONF").get("NAME", None)
                    if not access_verify(user_id=user_id, app_name=app_name, resource_code=resource_code):
                        raise PermissionDenied()
                return function(request, *args, **kwargs)
            return wrap
        method_list = [_.lower() for _ in resource.keys()]
        view.dispatch = method_decorator(func)(view.dispatch)
        return view
    return decorator
