from ._controller import RabbitMQConsumer
from sparrow_cloud.registry.service_discovery import consul_service
from sparrow_cloud.apps.message_service.aliyun_amqp import AliyunCredentialsProvider3 as aliyun_provider
from django.conf import settings
import time

def get_settings_value(name):
    """获取settings中的配置"""
    value = getattr(settings, name, None)
    if value == '' or value is None:
        raise NotImplementedError("没有配置这个参数%s" % name)
    return value


def rabbitmq_consumer(queue):
    """
    SparrowRabbitmpConsumer

        参数：
            queue # settings里面queue_conf 配置

        settings配置

        SPARROW_RABBITMQ_CONSUMER_CONF = {

            "MESSAGE_BROKER_CONF": {
                "USER_NAME": "hg_test",
                "PASSWORD": "jft87JheHe23",
                "VIRTUAL_HOST": "sparrow_test",
                "BROKER_SERVICE_CONF": {
                    "ENV_NAME": "SPARROW_BROKER_HOST",
                    "VALUE": "sparrow-demo",
                },
            },
            "ALIYUN_RABBITMQ_BROKER": {
                "HOST": "20882320.mq-amqp.cn-beijing-a.aliyuncs.com",
                "PORT": "5672",
                "VIRTUAL_HOST": 'sparrow_test',
                "ACCESS_KEY": "LTAI4FirPhTQuA5tYfY2JLEv",
                "ACCESS_SECRET": "xKvX9tWe8wkYmxwkaMiXL1LIe8hdq1",
                "RESOURCEOWNERID": 20882320,
                "SECURITY_TOKEN": "",
            }, 
            "RABBITMQ_SELECTION": "MESSAGE_BROKER_CONF",
            "MESSAGE_BACKEND_CONF": {
                "BACKEND_SERVICE_CONF": {
                        "ENV_NAME": "SPARROW_BACKEND_HOST",
                        "VALUE": "sparrow-demo",
                },
                "API_PATH": "/api/sparrow_task/task/update/"
            },
            "RETRY_TIMES": 3,
            "INTERVAL_TIME": 3,
            "HEARTBEAT": 600,
        }

        QUEUE_CONF_1 = {
            "QUEUE": "ORDER_PAY_SUC_ALL",
            "TARGET_FUNC_MAP": {
                "ORDER_PAY_SUC_ONLINE": "message_service.task.task1"
            }
        }


        ps:
                SPARROW_RABBITMQ_CONSUMER_CONF  # consumer的配置
                    MESSAGE_BROKER_CONF  # rabbitmq配置
                        USER_NAME # 用户名
                        PASSWORD # 密码
                        BROKER_SERVICE_CONF  # 依赖consul服务的配置
                    MESSAGE_BACKEND_CONF
                        BACKEND_SERVICE_CONF # 依赖consul服务的配置
                        API_PATH # api 路径
                    RETRY_TIMES # 错误重试次数，默认3次
                    INTERVAL_TIME   # 错误重试间隔，默认3秒
                    HEARTBEAT   # 消费者与rabbitmq心跳检测间隔，默认600秒
                QUEUE_CONF_1  # 队列的配置
                    QUEUE  # 队列名称
                    TARGET_FUNC_MAP  # 队列消费的任务（字典中的键为message code，
                                        对应的值为执行该消息的任务函数路径字符串）


    """
    consumer_conf = get_settings_value('SPARROW_RABBITMQ_CONSUMER_CONF')
    queue_conf = get_settings_value(queue)
    rabbitmq_selection = consumer_conf.get('RABBITMQ_SELECTION', "MESSAGE_BROKER_CONF")
    retry_times = consumer_conf.get('RETRY_TIMES', 3)
    interval_time = consumer_conf.get('INTERVAL_TIME', 3)
    consumer_heartbeat = consumer_conf.get('HEARTBEAT', 60)
    backend_service_conf = consumer_conf['MESSAGE_BACKEND_CONF']
    # broker_service_conf = consumer_conf['MESSAGE_BROKER_CONF'].get('BROKER_SERVICE_CONF', None)
    # broker_service_username = consumer_conf['MESSAGE_BROKER_CONF'].get('USER_NAME', None)
    # broker_service_password = consumer_conf['MESSAGE_BROKER_CONF'].get('PASSWORD', None)
    # virtual_host = consumer_conf['MESSAGE_BROKER_CONF'].get('VIRTUAL_HOST', None)
    
    while True:
        try:
            rabbitmq_conf = consumer_conf[rabbitmq_selection]
            virtual_host = rabbitmq_conf.get('VIRTUAL_HOST', None)
            if rabbitmq_selection == "ALIYUN_RABBITMQ_BROKER":
                # 连接aliyun amqp
                host = rabbitmq_conf["HOST"]
                port = rabbitmq_conf["PORT"]
                accessKey = rabbitmq_conf["ACCESS_KEY"]
                accessSecret = rabbitmq_conf["ACCESS_SECRET"]
                resourceOwnerId = rabbitmq_conf["RESOURCEOWNERID"]
                # security_token = rabbitmq_conf["SECURITY_TOKEN"]
                provider = aliyun_provider.AliyunCredentialsProvider(accessKey, accessSecret, resourceOwnerId)
                username = provider.get_username()
                password = provider.get_password()
            else:
                broker_service_conf = rabbitmq_conf.get('BROKER_SERVICE_CONF', None)
                username = rabbitmq_conf.get('USER_NAME', None)
                password = rabbitmq_conf.get('PASSWORD', None)
                broker_service_addr = consul_service(broker_service_conf)
                host = broker_service_addr.split(':')[0]
                port = broker_service_addr.split(':')[1]

            message_broker_conf = {
                "host": host,
                "port": port,
                "username": username,
                "password": password,
                "virtual_host": virtual_host,
            }
            if backend_service_conf:
                consumer = RabbitMQConsumer(
                    queue=queue_conf.get('QUEUE', None),
                    message_broker_conf=message_broker_conf,
                    message_backend_conf=backend_service_conf,
                    retry_times=retry_times,
                    interval_time=interval_time,
                    heartbeat=consumer_heartbeat
                )
            else:
                consumer = RabbitMQConsumer(
                    queue=queue_conf.get('QUEUE', None),
                    message_broker_conf=message_broker_conf,
                    retry_times=retry_times,
                    interval_time=interval_time,
                    heartbeat=consumer_heartbeat)
            consumer.target_func_map = queue_conf.get('TARGET_FUNC_MAP', None)
            consumer.consume()
        except KeyboardInterrupt:
            break
        except:
            # 如果遇到exception不退出，过几秒重试一下
            time.sleep(interval_time)
