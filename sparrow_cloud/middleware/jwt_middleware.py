# -*- coding: utf-8 -*-
from rest_framework.authentication import get_authorization_header
from sparrow_cloud.utils.decode_jwt import decode_jwt
from sparrow_cloud.middleware.base.base_middleware import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)


class JWTMiddleware(MiddlewareMixin):

    def process_request(self, request):
        '''
        HTTP_AUTHORIZATION': 'Token eyJhbGciOiJIU.eyJpc3MiOiWTy.z0HODSJhWtFzX'
        '''
        auth = get_authorization_header(request).split()
        # 如果没有token, 返回空
        if not auth or auth[0].lower() != b'token':
            request.META['REMOTE_USER'] = None
            request.META['payload'] = None
            return 
        try:
            token = auth[1]
            payload = decode_jwt(token)
            payload["token"] = str(token, encoding='utf-8')
            user_id = payload["uid"]
            request.META['REMOTE_USER'] = user_id
            request.META['payload'] = payload
        except Exception as ex:
            logger.error(ex)
            request.META['REMOTE_USER'] = None
            request.META['payload'] = None
