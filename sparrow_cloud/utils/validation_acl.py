# import jwt
# from django.conf import settings
#
#
# def get_acl_private_key():
#     # ACL_MIDDLEWARE = {
#     #     "ACL_SERVICE": {
#     #         # ENV_NAME 为覆盖consul的默认值, 环境变量名称示例：服务名称_HOST， 只需要给一个环境变量的NAME，不需要给VALUE
#     #         "ENV_NAME": "SPARROW_SERVICE_ACL_HOST",
#     #         # VALUE 为服务发现的注册名称
#     #         "VALUE": os.environ.get("SPARROW_SERVICE_ACL_SVC", "sparrow_service_acl_svc"),
#     #     },
#     #     "API_PATH": "/api/v1/service_acl/acl_token/",
#     #     "ACL_PRIVATE_KEY": ""
#     # }
#
#     acl_middleware_value = getattr(settings, 'ACL_MIDDLEWARE', None)
#     if acl_middleware_value:
#         acl_private_key = acl_middleware_value.get('ACL_PRIVATE_KEY', None)
#         if acl_private_key is None and acl_private_key == '':
#             raise Exception("ACL_MIDDLEWARE 未配置: ACL_PRIVATE_KEY")
#         return acl_private_key
#     raise Exception("ACL_MIDDLEWARE 未配置: ACL_PRIVATE_KEY")
#
#
# def acl_validated(acl_token):
#     """validated acl token"""
#     public_key = get_acl_private_key()
#     try:
#         jwt.decode(acl_token, public_key, algorithms='RS256')
#         return True
#     except ValueError as ex:
#         return False


import jwt
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def get_acl_public_key():
    """get acl public """
    acl_middleware_value = getattr(settings, 'ACL_MIDDLEWARE', None)
    if acl_middleware_value:
        acl_private_key = acl_middleware_value.get('ACL_PUBLIC_KEY', None)
        if acl_private_key is None and acl_private_key == '':
            logging.error('sparrow_cloud error: ACL_PUBLIC_KEY not configured in ACL_MIDDLEWARE')
            raise Exception("sparrow_cloud error: ACL_PUBLIC_KEY not configured in ACL_MIDDLEWARE")
        return acl_private_key
    logging.error('sparrow_cloud error: ACL_MIDDLEWARE not configured')
    raise Exception("sparrow_cloud error: ACL_MIDDLEWARE not configured")


def validation_acl(acl_token):
    """validation acl token"""
    public_key = get_acl_public_key()
    try:
        payload = jwt.decode(acl_token, public_key, algorithms='RS256')
        logging.info('sparrow_cloud: acl_validated:{}'.format(payload))
        return True, payload
    except Exception as ex:
        logging.info('sparrow_cloud: validation error, acl_token:{}'.format(acl_token))
        return False, {}
