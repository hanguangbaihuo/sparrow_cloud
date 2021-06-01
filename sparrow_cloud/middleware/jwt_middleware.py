# -*- coding: utf-8 -*-
import base64
import json
import os
from rest_framework.authentication import get_authorization_header
from sparrow_cloud.utils.decode_jwt import decode_jwt
from sparrow_cloud.middleware.base.base_middleware import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)

algorithms = ["HS256", "RS256"]

class JWTMiddleware(MiddlewareMixin):

    def process_request(self, request):
        '''
        HTTP_AUTHORIZATION': 'Token eyJhbGciOiJIU.eyJpc3MiOiWTy.z0HODSJhWtFzX'
        '''
        auth = get_authorization_header(request).split()
        # 如果没有token, 返回空
        if not auth or auth[0].lower() != b'tokentest':
            request.META['REMOTE_USER'] = None
            request.META['payload'] = None
            return

        token = auth[1]
        try:
            flag = False
            for algorithm in algorithms:
                # 对称加密，从环境变量获取密钥
                if algorithm == "HS256":
                    secret = os.getenv("JWT_SECRET")
                # 非对称加密，从环境变量获取公钥文件路径
                else:# elif algorithm == "RS256":
                    public_key_path = os.getenv("PUBLIC_KEY_PATH")
                    secret = open(public_key_path).read()
                try:
                    payload = decode_jwt(token, secret, algorithm)
                    payload["token"] = token.decode('utf-8')
                    flag = True
                    logger.debug(f"本次解码方法:{algorithm}")
                    break
                except Exception as e:
                    pass
            # jwt正确解码
            if flag:
                user_id = payload["uid"]
                request.META['REMOTE_USER'] = user_id
                request.META['payload'] = payload
                # 对payload进行base64编码
                b64_payload = base64.b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8')
                request.META['X-Jwt-Payload'] = b64_payload
            else:
                raise Exception("找不到正确的jwt token解码方法或者token失效")
        except Exception as ex:
            logger.error(ex)
            request.META['REMOTE_USER'] = None
            request.META['payload'] = None
