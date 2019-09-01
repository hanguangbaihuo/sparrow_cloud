# -*- coding: utf-8 -*-

from rest_framework.exceptions import APIException
from rest_framework import status

class HTTP5XXException(APIException):
    pass


class HTTP4XXException(APIException):
    pass


class HTTPException(APIException):
    pass