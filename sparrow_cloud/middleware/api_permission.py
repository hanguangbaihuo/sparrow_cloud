import requests
import logging

from django.http import JsonResponse
from django.core.exceptions import ImproperlyConfigured

from sparrow_cloud.utils.validation_data import VerificationConfiguration
from sparrow_cloud.registry.service_registry import consul_service
from sparrow_cloud.utils.get_settings_value import GetSettingsValue
from sparrow_cloud.middleware.base.base_middleware import MiddlewareMixin
from sparrow_cloud.utils.normalize_url import NormalizeUrl

logger = logging.getLogger(__name__)


class PermissionMiddleware(MiddlewareMixin):
    """
    权限中间件
    使用方法：
        1.导入此文件到项目中
        2.将此中间件放在 AuthenticationMiddleware 之后
    工作原理：
                                (url + method + user_id)
                                        |               / 有权限则允许通过
    request -> PermissionMiddleware ---https---> 权限模块
                                                        \ 无权限则返回HTTP 403错误
    """
    VERIFICATION_CONGIGURATION = VerificationConfiguration()
    VERIFICATION_CONGIGURATION.valid_permission_svc()
    SETTINGS_VALUE = GetSettingsValue()
    URL_JOIN = NormalizeUrl()
    FILTER_PATH = SETTINGS_VALUE.get_middleware_value(
        'PERMISSION_MIDDLEWARE', 'FILTER_PATH')
    HAS_PERMISSION = True
    SKIP_PERMISSION = SETTINGS_VALUE.get_value('PERMISSION_MIDDLEWARE', 'SKIP_PERMISSION')

    def process_request(self, request):
        path = request.path
        method = request.method.upper()
        # 是否跳过中间件， true跳过， false不跳过
        if self.SKIP_PERMISSION is False:
            # 只校验有 不在 FILTER_PATH 中的url
            if path not in self.FILTER_PATH:
                if request.META['REMOTE_USER']:
                    self.HAS_PERMISSION = self.valid_permission(path, method, request.META['REMOTE_USER'])
                if not self.HAS_PERMISSION:
                    return JsonResponse({"message": "无访问权限"}, status=403)

    def valid_permission(self, path, method, user_id):
        """ 验证权限， 目前使用的是http的方式验证，后面可能要改成rpc的方式"""
        if all([path, method, user_id]):
            permission_service = GetSettingsValue().get_middleware_value('PERMISSION_MIDDLEWARE', 'PERMISSION_SERVICE')
            if permission_service['HOST']:
                service_conf = {
                    "NAME_SVC": permission_service['NAME'],
                    "HOST": permission_service['HOST'] + ':' + str(permission_service['PORT']),
                }
            else:
                service_conf = {
                    "NAME_SVC": permission_service['NAME'],
                    "HOST": "",
                }
            domain = consul_service(service_conf)
            url_path = self.URL_JOIN.normalize_url(
                domain=domain, path=permission_service['PATH'])
            url = url_path + '?userid={0}&path={1}&method={2}'.format(user_id, path, method)
            try:
                response = requests.get(url)
            except Exception as ex:
                logger.error(ex)
                return True
            if response.status_code == 404:
                raise ImproperlyConfigured(
                    "请检查settings.py的permission_service配置的%s是否正确" % permission_service['PATH'])
            data = response.json()
            if response.status_code == 500:
                logger.error(data["message"])
                return True
            if 200 <= response.status_code < 300 and data['status']:
                return True
            return False