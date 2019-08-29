from sparrow_django_common.utils.get_settings_value import GetSettingsValue
from sparrow_django_common.base_middlware.base_middleware import MiddlewareMixin


get_value = GetSettingsValue()
METHOD_MAP = get_value.get_middleware_value('METHOD_MIDDLEWARE', 'METHOD_MAP')
if not METHOD_MAP:
    METHOD_MAP = ('PUT', 'DELETE')


class MethodConvertMiddleware(MiddlewareMixin):
    """解决阿里云不支持put/delete 请求方式的问题"""
    def process_request(self, request):
        if 'HTTP_METHOD' in request.META:
            method = request.META['HTTP_METHOD'].upper()
            if method in METHOD_MAP:
                setattr(request, 'method', method)
