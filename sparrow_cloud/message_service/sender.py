from django.conf import settings
from .sender_controller import TaskSender
# from sparrow_cloud.registry.service_discovery import consul_service
from sparrow_cloud.restclient.exception import HTTPException

from functools import lru_cache
import time
#
# @lru_cache(maxsize=None)
# def get_tasks_sender_object(message_backend):
#     task_sender = TaskSender(message_backend)
#     return task_senderml


def get_settings_value(name):
    """获取settings中的配置"""
    value = getattr(settings, name, None)
    if value == '' or value is None:
        raise NotImplementedError("没有配置这个参数%s" % name)
    return value


def send_task(exchange, routing_key, message_code, retry_times=3, *args, **kwargs):
    """
    发送实时任务
        参数：
            exchange/routing_key/message_code, 创建消息服务时返回的配置信息
            *args
            **kwargs
        settings配置：

        MESSAGE_SENDER_CONF = {
            "SERVICE_CONF": "xxxxx-svc:8000",
            "API_PATH": "/api/sparrow_task/producer/send/",
        }

    """
    message_conf = get_settings_value("MESSAGE_SENDER_CONF")
    task_sender = TaskSender(message_conf)
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
        settings配置：

        MESSAGE_SENDER_CONF = {
            "SERVICE_CONF": {
                "ENV_NAME": "DLJFLS_LSDK_LDKEND",
                "VALUE": "xxxxx-svc",
            },
            "API_PATH": "/api/sparrow_task/producer/send/",
        }

    """
    message_conf = get_settings_value("MESSAGE_SENDER_CONF")
    task_sender = TaskSender(message_conf)
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
        settings配置：

        TASK_PROXY_CONF = {
            "SERVICE_CONF": "xxxxx-svc:8001",
            "API_PATH": "/api/sparrow_task_proxy/producer/send",
        }

    """
    message_conf = get_settings_value("TASK_PROXY_CONF")
    task_sender = TaskSender(message_conf)
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