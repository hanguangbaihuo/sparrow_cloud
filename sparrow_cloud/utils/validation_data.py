from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class VerificationConfiguration(object):
    """验证中间件需要配置"""

    def __valid_permission_svc(self):
        """验证settings中的配置, 如有新增的配置，请在此处加上验证"""
        try:
            self.PERMISSION_SERVICE = settings.PERMISSION_MIDDLEWARE['PERMISSION_SERVICE']
            self.FILTER_PATH = settings.PERMISSION_MIDDLEWARE['FILTER_PATH']
            self.PERMISSION_SERVICE['NAME']
            self.PERMISSION_SERVICE['HOST']
            self.PERMISSION_SERVICE['PATH']
        except KeyError as ex:
            raise NotImplementedError("没有配置这个参数%s"% ex)

    def __verify_middleware_location(self, request):
        """验证中间件位置"""
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "PermissionMiddleware应该放置在'sparrow_cloud.middleware.jwt_middleware.JWTMiddleware'后面")

    def valid_permission_svc(self):
        """settings配置数据校验"""
        self.__valid_permission_svc()

    def verify_middleware_location(self, request):
        """校验中间件位置"""
        self.__verify_middleware_location(request)
