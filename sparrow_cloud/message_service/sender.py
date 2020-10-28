from django.conf import settings
from .sender_controller import TaskSender
from sparrow_cloud.restclient.exception import HTTPException
from sparrow_cloud.utils.get_cm_value import get_cm_value

from functools import lru_cache
import time
#
# @lru_cache(maxsize=None)
# def get_tasks_sender_object(message_backend):
#     task_sender = TaskSender(message_backend)
#     return task_senderml


def send_task(exchange, routing_key, message_code, retry_times=3, *args, **kwargs):
    """
    发送实时任务
        参数：
            exchange/routing_key/message_code, 创建消息服务时返回的配置信息
            *args
            **kwargs

    configmap ：
        SC_MESSAGE_SENDER_SVC: "xxxxxxx-svc:8000"
        SC_MESSAGE_SENDER_API: "/api/sparrow_task/producer/send/"
    """
    sc_message_sender_svc = get_cm_value("SC_MESSAGE_SENDER_SVC")
    sc_message_sender_api = get_cm_value("SC_MESSAGE_SENDER_API")
    task_sender = TaskSender(sc_message_sender_svc=sc_message_sender_svc, sc_message_sender_api=sc_message_sender_api)
    # 发送任务出现异常时的初始重试时间间隔
    interval_time = 1
    error_message = None
    for _ in range(retry_times):
        try:
            task_result = task_sender.send_task(
                    exchange=exchange,
                    routing_key=routing_key,
                    message_code=message_code,
                    *args,
                    **kwargs
                )
            return task_result
        except Exception as ex:
            time.sleep(interval_time)
            error_message = ex.__str__()
    raise Exception("消息发送失败，失败原因{},重试次数{}，消息内容message_code={},消息参数{}{}".format(
                    error_message, retry_times, message_code, args, kwargs))



def send_task_v2(message_code, retry_times=3, *args, **kwargs):
    """
    发送实时任务
        参数：
            message_code 消息代码 
            *args
            **kwargs
        configmap :
            SC_TASK_PROXY: xxxxx-svc:8000
            SC_TASK_PROXY_API: "/api/xxxxxxxxxx/producer/send/"
    """
    sc_task_proxy = get_cm_value("SC_TASK_PROXY")
    sc_task_proxy_api = get_cm_value("SC_TASK_PROXY_API")
    task_sender = TaskSender(sc_message_sender_svc=sc_task_proxy, sc_message_sender_api=sc_task_proxy_api)
    # 发送任务出现异常时的初始重试时间间隔
    interval_time = 1
    error_message = None
    for _ in range(retry_times):
        try:
            task_result = task_sender.send_task(
                    exchange=None,
                    routing_key=None,
                    message_code=message_code,
                    delay=False,
                    *args,
                    **kwargs
                )
            return task_result
        except Exception as ex:
            time.sleep(interval_time)
            error_message = ex.__str__()
    raise Exception("消息发送失败，失败原因{},重试次数{}，消息内容message_code={},消息参数{}{}".format(
                    error_message, retry_times, message_code, args, kwargs))


def send_task_v3(message_code, *args, **kwargs):
    """
    发送实时任务
        参数：
            message_code 消息代码 
            *args
            **kwargs
        configmap :
            SC_TASK_PROXY: xxxxx-svc:8000
            SC_TASK_PROXY_API: "/api/xxxxxxxxxx/producer/send/"
    """
    sc_task_proxy = get_cm_value("SC_TASK_PROXY")
    sc_task_proxy_api = get_cm_value("SC_TASK_PROXY_API")
    task_sender = TaskSender(sc_message_sender_svc=sc_task_proxy, sc_message_sender_api=sc_task_proxy_api)
    error_message = None
    try:
        task_result = task_sender.send_task(
                exchange=None,
                routing_key=None,
                message_code=message_code,
                delay=False,
                *args,
                **kwargs
            )
        return task_result
    except Exception as ex:
        error_message = ex.__str__()
        raise Exception("消息发送失败，失败原因{}, 消息内容message_code={},消息参数{}{}".format(
                    error_message, message_code, args, kwargs))