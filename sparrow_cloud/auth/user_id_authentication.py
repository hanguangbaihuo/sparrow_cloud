# -*- coding: utf-8 -*-
import base64
import json
import logging
from sparrow_cloud.utils.get_user import get_user_class


logger = logging.getLogger(__name__)

# default user: sparrow_cloud.auth.user.User
USER_CLASS = get_user_class()

class UserIDAuthentication(object):

    def authenticate(self, request):
        '''
        get X-Jwt-Payload header from gateway. It is base64 encoding of payload data.
        X-Jwt-Payload: 'eyJ1aWQiOiAiMTIzNGFiYyIsICJleHAiOiAxNzIyMjAwMzE2LCAiaWF0IjogMTYyMjE5MzExNiwgImFwcF9pZCI6ICJjb3JlIn0='
        payload: {'uid': '1234abc', 'exp': 1722200316, 'iat': 1622193116, 'app_id': 'core'}
        here text format coding should be compatible, in order to test api locally.
        e.g.
        X-Jwt-Payload: "{'uid': '1234abc', 'exp': 1722200316, 'iat': 1622193116, 'app_id': 'core'}"
        '''
        request.META.setdefault("X-Jwt-Payload", request.META.get("HTTP_X_JWT_PAYLOAD"))
        raw_data = request.META.get("X-Jwt-Payload")
        if not raw_data:
            return None
        try:
            # 先通过base64编码进行解析
            b64_payload = base64.b64decode(raw_data)
            payload = json.loads(b64_payload)
        except Exception as e:
            # 解析出错，再通过text文本进行解析
            try:
                payload = json.loads(raw_data)
            except Exception as e:
                logger.error(f"X-Jwt-Payload:{raw_data}无法解析")
                return None
        try:
            user_id = payload.get("uid")
            if not user_id:
                logger.error(f"payload中没有uid:{payload}")
                return None
            # 兼容一些业务中采用REMOTE_USER获取uid
            request.META['REMOTE_USER'] = user_id
            request.META['payload'] = payload
            user = self.get_user(user_id, payload)
            return (user, payload)
        except Exception as e:
            logger.error(e)
            return None

    def get_user(self, user_id, payload):
        user = USER_CLASS(user_id,payload)
        return user

    def authenticate_header(self, request):
        return "Token"