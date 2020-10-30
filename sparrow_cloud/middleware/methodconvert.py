from json import loads

from sparrow_cloud.utils.get_cm_value import get_cm_value
from sparrow_cloud.middleware.base.base_middleware import MiddlewareMixin

sc_method_map = get_cm_value("SC_METHOD_MAP")
METHOD_MAP = tuple(loads(sc_method_map).values())
if not METHOD_MAP:
    METHOD_MAP = ('PUT', 'DELETE')


class MethodConvertMiddleware(MiddlewareMixin):
    """解决阿里云不支持put/delete 请求方式的问题"""
    def process_request(self, request):
        if 'HTTP_METHOD' in request.META:
            method = request.META['HTTP_METHOD'].upper()
            if method in METHOD_MAP:
                setattr(request, 'method', method)
