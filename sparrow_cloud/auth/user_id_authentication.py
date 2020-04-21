# -*- coding: utf-8 -*-
from sparrow_cloud.utils.get_user import get_user_class
import logging

logger = logging.getLogger(__name__)


class UserIDAuthentication(object):

    USER_CLASS = get_user_class()

    def authenticate(self, request):
        '''
        HTTP_AUTHORIZATION': 'Token eyJhbGciOiJIU.eyJpc3MiOiWTy.z0HODSJhWtFzX'
        try to create user Model from UserModel
            if suc : return user
            if falied: return None
        '''
        payload = request.META['payload']
        user_id = request.META['REMOTE_USER']
        if payload and user_id:
            try:
                user = self.get_user(user_id, payload)
            except Exception as ex:
                logger.error(ex)
                return None
            return (user, payload)
        return None

    def get_user(self, user_id, payload):
        user = self.USER_CLASS(user_id=user_id)
        user.payload = payload
        return user

    def authenticate_header(self, request):
        return "Token"