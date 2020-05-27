class BaseException(Exception):
    pass


class PermissionValidError(BaseException):
    """自定义异常"""
    pass


class AuthenticationValidError(BaseException):
    """自定义异常"""
    pass


class ResourceValidError(BaseException):
    """自定义异常"""
    pass
