# -*- coding: utf-8 -*-

from rest_framework.exceptions import APIException
from rest_framework import status


class HTTPException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = ''
    default_code = ''

    def __init__(self, detail=None, code=None):
        '''
        为了兼容 drf 3.4: APIException 没有 code 初始化参数
        '''
        try:
            # drf 3.10
            super(HTTPException, self).__init__(detail=detail, code=code)
        except:
            # drf 3.4
            super(HTTPException, self).__init__(detail=detail)