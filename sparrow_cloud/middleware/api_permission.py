import logging
from django.http import JsonResponse
from sparrow_cloud.utils.validation_data import VerificationConfiguration
from sparrow_cloud.utils.get_settings_value import GetSettingsValue
from sparrow_cloud.middleware.base.base_middleware import MiddlewareMixin
from sparrow_cloud.utils.normalize_url import NormalizeUrl
from sparrow_cloud.restclient import rest_client
from sparrow_cloud.restclient.exception import HTTPException

logger = logging.getLogger(__name__)


class PermissionMiddleware(MiddlewareMixin):
    """
    权限中间件
    使用方法：
        1.导入此文件到项目中
        2.将此中间件放在 AuthenticationMiddleware 之后
    工作原理：
                                (url + method + user_id)
                                        |                - 有权限则允许通过
    request -> PermissionMiddleware ---https---> 权限模块|
                                                         - 无权限则返回HTTP 403错误
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
                    msg = "{},{},{}".format(path, method, request.META['REMOTE_USER'])
                    logging.info(msg)
                    try:
                        if not self.valid_permission(path, method, request.META['REMOTE_USER']):
                            return JsonResponse({"message": "无访问权限"}, status=403)
                    except HTTPException as ex:
                        if ex.status_code >= 500:
                            logger.error("permission is not avaiable. detail={}".format(ex.detail))
                            return
                        elif ex.status_code >= 300:
                            msg = "中间件调用错误: {},status_code={}".format(ex.detail, ex.status_code)
                            return JsonResponse({"message": msg}, status=400)

    def valid_permission(self, path, method, user_id):
        """ 验证权限， 目前使用的是http的方式验证，后面可能要改成rpc的方式"""
        if all([path, method, user_id]):
            service_conf = GetSettingsValue().get_middleware_value('PERMISSION_MIDDLEWARE', 'PERMISSION_SERVICE')
            api_path = self.SETTINGS_VALUE.get_middleware_value('PERMISSION_MIDDLEWARE', 'API_PATH')
            payload = {
                "method": method,
                "path": path,
                "user_id": user_id,
            }
            try:
                response = rest_client.get(service_conf, api_path=api_path, params=payload)
                if 200 <= response['status_code'] < 300 and response['has_perm']:
                    return True
                else:
                    logger.info("something is wrong. {}".format(response))
                    return False
            except HTTPException as ex:
                raise ex
        return False
