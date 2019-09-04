# # 发送非延时任务
from task_sender import TaskSender
# from sparrow_cloud.registry.service_registry import consul_service


#
# MESSAGE_CLIENT_CONF = {
#     "SERVICE_REGISTER_NAME": "",
#     "HOST": "127.0.0.1:8001"
# }


def message_client(exchange, routing_key, message_code, *args, **kwargs):
    """发送非延时任务"""
    message_backend = "sparrow-task-test-svc:8001/api/sparrow_task/producer/send/"
    task_sender = TaskSender(message_backend)
    task_sender.send_task(
            exchange=exchange,
            routing_key=routing_key,
            message_code=message_code,
            *args,
            **kwargs
        )
