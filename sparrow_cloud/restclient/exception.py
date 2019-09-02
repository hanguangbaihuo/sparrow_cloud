# -*- coding: utf-8 -*-

from rest_framework.exceptions import APIException
from rest_framework import status

class HTTP5XXException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'permission not register'
    default_code = 'PERMISSION_NOT_REGISTER'


class HTTP4XXException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'permission not register'
    default_code = 'PERMISSION_NOT_REGISTER'


class HTTPException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'permission not register'
    default_code = 'PERMISSION_NOT_REGISTER'