# -*- coding: utf-8 -*-
from django.http import JsonResponse
from sparrow_cloud.utils.validation_acl import validation_acl
from sparrow_cloud.middleware.base.base_middleware import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)


class ACLMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """
        ACL VALIDATE
        验证步骤：
            1: 获取：REMOTE_USER 和 acl_token
            如果没有acl_token 放行
            如果有remote_user，acl_token通过验证，放行，否则403
            如果没有remote_user，acl_token通过验证，放行，否则403
        :param request:
        :return:
        """
        remote_user = request.META.get('REMOTE_USER', None)
        acl_token = request.GET.get('acl_token', None)
        if not acl_token:
            return
        data = request.GET
        data._mutable = True   # 更改为True ，数据可修改
        data.pop('acl_token')
        data._mutable = False  # 修改数据后还原mutable为False
        validate, payload = validation_acl(acl_token)
        if remote_user:
            if acl_token and validate:
                return
            if acl_token and validate is False:
                return JsonResponse({"message": "ACL验证未通过"}, status=403)
        elif not remote_user:
            if acl_token and validate:
                request.META['REMOTE_USER'] = acl_token
                request.META['payload'] = payload
                return
            if acl_token and validate is False:
                return JsonResponse({"message": "ACL验证未通过"}, status=403)
        else:
            raise Exception('ACL_MIDDLEWARE ERROR: Unknown situation')

