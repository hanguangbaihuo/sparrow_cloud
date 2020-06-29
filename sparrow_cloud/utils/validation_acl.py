# import jwt
# import logging
# from django.conf import settings
#
# logger = logging.getLogger(__name__)
#
#
# def get_acl_public_key():
#     """get acl public """
#     acl_middleware_value = getattr(settings, 'ACL_MIDDLEWARE', None)
#     if acl_middleware_value:
#         acl_private_key = acl_middleware_value.get('ACL_PUBLIC_KEY', None)
#         if acl_private_key is None or acl_private_key == '':
#             logging.error('sparrow_cloud error: ACL_PUBLIC_KEY not configured in ACL_MIDDLEWARE')
#             raise Exception("sparrow_cloud error: ACL_PUBLIC_KEY not configured in ACL_MIDDLEWARE")
#         return acl_private_key
#     logging.error('sparrow_cloud error: ACL_MIDDLEWARE not configured')
#     raise Exception("sparrow_cloud error: ACL_MIDDLEWARE not configured")
#
#
# def validation_acl(acl_token):
#     """validation acl token"""
#     public_key = get_acl_public_key()
#     try:
#         payload = jwt.decode(acl_token, public_key, algorithms='RS256')
#         logging.info('sparrow_cloud: acl_validated:{}'.format(payload))
#         return True, payload
#     except Exception as ex:
#         logging.info('sparrow_cloud: validation error, acl_token:{}'.format(acl_token))
#         return False, {}
