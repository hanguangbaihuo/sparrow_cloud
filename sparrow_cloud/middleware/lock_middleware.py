from django.http import JsonResponse
import logging
from sparrow_cloud.middleware.base.base_middleware import MiddlewareMixin
from sparrow_cloud.utils.get_cm_value import get_cm_value
from sparrow_cloud.restclient import rest_client

logger = logging.getLogger(__name__)

class CheckLockMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # key = request.headers.get("Sc-Lock")
        key = request.META.get("HTTP_SC_LOCK")
        # key不存在或者值为空，跳过锁检查，放行
        if not key:
            return
        SC_SPARROW_DISTRIBUTED_LOCK_SVC = get_cm_value("SC_SPARROW_DISTRIBUTED_LOCK_SVC")
        SC_SPARROW_DISTRIBUTED_LOCK_FRONT_API = get_cm_value("SC_SPARROW_DISTRIBUTED_LOCK_FRONT_API")
        try:
            response = rest_client.delete(SC_SPARROW_DISTRIBUTED_LOCK_SVC, SC_SPARROW_DISTRIBUTED_LOCK_FRONT_API, json={"key":key})
            res = response.get("result")
            if res: # result不是0,则表示key存在且删除成功，只有在key存在的情况下表明是第一次提交，之后的提交会由于key不存在而禁止
                return
            else: # 锁不存在，可能已经被删除或者超时过期
                return JsonResponse({"message":"重复提交，本次操作被禁止"}, status=403)
        except Exception as e:
            logger.info("check front lock failed in lock middleware, message: {}".format(e.__str__()))
            return