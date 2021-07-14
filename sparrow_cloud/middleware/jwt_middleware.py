# -*- coding: utf-8 -*-
# import base64
# from django.conf import settings
import json
import os
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

        token = auth[1]
        try:
            payload = decode_jwt(token, os.getenv("SC_JWT_PUBLIC_KEY"), "RS256")
            payload["token"] = token.decode('utf-8')
            user_id = payload.get("uid")
            request.META['REMOTE_USER'] = user_id
            request.META['payload'] = payload
            # 对payload进行base64编码
            # b64_payload = base64.b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8')
            # request.META['X-Jwt-Payload'] = b64_payload
            request.META['X-Jwt-Payload'] = json.dumps(payload)
        except Exception as ex:
            logger.error(ex)
            request.META['REMOTE_USER'] = None
            request.META['payload'] = None
