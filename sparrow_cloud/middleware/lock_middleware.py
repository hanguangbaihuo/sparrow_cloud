from django.http import JsonResponse
import logging
from sparrow_cloud.middleware.base.base_middleware import MiddlewareMixin
from sparrow_cloud.utils.get_cm_value import get_cm_value
from sparrow_cloud.restclient import rest_client

logger = logging.getLogger(__name__)

SC_SPARROW_DISTRIBUTED_LOCK_SVC = get_cm_value("SC_SPARROW_DISTRIBUTED_LOCK_SVC")
SC_SPARROW_DISTRIBUTED_LOCK_FRONT_API = get_cm_value("SC_SPARROW_DISTRIBUTED_LOCK_FRONT_API")

class CheckLockMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # key = request.headers.get("Sc-Lock")
        key = request.META.get("HTTP_SC_LOCK")
        # key不存在或者值为空，跳过锁检查，放行
        if not key:
            return
        try:
            response = rest_client.put(SC_SPARROW_DISTRIBUTED_LOCK_SVC, SC_SPARROW_DISTRIBUTED_LOCK_FRONT_API, json={"key":key,"opt":"incr"})
            res = response.get("code")
            # 只有当锁存在且其值为0(表示锁未被使用)时，code才会返回0
            if res==0:
                return
            else: # 锁不存在(被删除或者超时过期)或者其值不为0(表示已经使用)时，禁止本次操作。返回状态码不用403是为了防止前端由于4xx状态而弹出通知，静默防重复提交。
                return JsonResponse({"message":"重复提交，本次操作被禁止", "code":233402}, status=200)
        except Exception as e:
            # 发生异常时，直接放行
            logger.info("check front lock failed in lock middleware, message: {}".format(e.__str__()))
            return

    def process_response(self, request, response):
        key = request.META.get("HTTP_SC_LOCK")
        if not key:
            return response
        # 业务处理正常，删除锁中的key
        if response.status_code>=200 and response.status_code<300:
            rest_client.delete(SC_SPARROW_DISTRIBUTED_LOCK_SVC, SC_SPARROW_DISTRIBUTED_LOCK_FRONT_API, json={"key":key})
        else:#业务失败，重置锁，可以进行下一次请求
            rest_client.put(SC_SPARROW_DISTRIBUTED_LOCK_SVC, SC_SPARROW_DISTRIBUTED_LOCK_FRONT_API, json={"key":key,"opt":"reset"})
        return response