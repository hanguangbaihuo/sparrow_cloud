# from rabbitmq_consumer import RabbitMQConsumer
# from sparrow_cloud.registry.service_discovery import consul_service
# from django.conf import settings
#
#
# def get_settings_value(name):
#     """获取settings中的配置"""
#     value = getattr(settings, name, None)
#     if value == '' or value is None:
#         raise NotImplementedError("没有配置这个参数%s" % name)
#     return value
#
#
# def rabbitmq_consumer(queue):
#     """
#     SparrowRabbitmpConsumer
#
#         参数：
#             queue # settings里面queue_conf 配置
#
#         settings配置
#
#             SPARROW_RABBITMQ_CONSUMER_CONF = {
#                 "SERVICE_CONF": {
#                         "ENV_NAME": "DLJFLS_LSDK_LDKEND",
#                         "VALUE": "xxxxx-svc",
#                     },
#                 "MESSAGE_BROKER": "",
#                 "MESSAGE_BACKEND": "",
#             }
#
#             QUEUE_CONF_1 = {
#                 "QUEUE": "XXX",
#                 "TARGET_FUNC_MAP : {
#                     "xxx": "xx.xx"
#                 }
#             }
#             ps:
#                 SPARROW_RABBITMQ_CONSUMER_CONF  # consumer的配置
#                     SERVICE_CONF  # 如果配置了MESSAGE_BACKEND， 则需要配置SERVICE_CONF， consul依赖
#                     MESSAGE_BROKER  # 必填 rabbitmq 的地址
#                     MESSAGE_BACKEND # 选填的配置，如果设置了message_backend,则在任务执行完成之后会向该
#                                       设置里的url发送任务执行完成结果，post请求
#                 QUEUE_CONF_1  # 队列的配置
#                     QUEUE  # 队列名称
#                     TARGET_FUNC_MAP  # 队列消费的任务（字典中的键为message code，
#                                         对应的值为执行该消息的任务函数路径字符串）
#
#
#     """
#     consumer_conf = get_settings_value('SPARROW_RABBITMQ_CONSUMER_CONF')
#     queue_conf = get_settings_value(queue)
#     message_backend = consumer_conf.get('message_backend', None)
#     SERVICE_CONF = consumer_conf.get('SERVICE_CONF', None)
#     if consumer_conf.get('message_backend', None)
#     # if message_backend:
#     #     if consumer_conf
#     consumer = RabbitMQConsumer(
#         queue=queue_conf.get('queue', None),
#         message_broker=consumer_conf.get('message_broker', None),
#         message_backend=consumer_conf.get('message_backend', None)
#     )
#     consumer.target_func_map = queue_conf.get('target_func_map', None)
#     consumer.consume()
