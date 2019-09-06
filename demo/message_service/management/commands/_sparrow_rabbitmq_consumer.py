from rabbitmq_consumer import RabbitMQConsumer
from sparrow_cloud.registry.service_discovery import consul_service
from django.conf import settings


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
                "BROKER_SERVICE_CONF": {
                    "ENV_NAME": "SPARROW_BROKER_HOST",
                    "VALUE": "sparrow-demo",
                },
            },
            "MESSAGE_BACKEND_CONF": {
                "BACKEND_SERVICE_CONF": {
                        "ENV_NAME": "SPARROW_BACKEND_HOST",
                        "VALUE": "sparrow-demo",
                },
                "API_PATH": "/api/sparrow_task/task/update/"
            }
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
                QUEUE_CONF_1  # 队列的配置
                    QUEUE  # 队列名称
                    TARGET_FUNC_MAP  # 队列消费的任务（字典中的键为message code，
                                        对应的值为执行该消息的任务函数路径字符串）


    """
    consumer_conf = get_settings_value('SPARROW_RABBITMQ_CONSUMER_CONF')
    queue_conf = get_settings_value(queue)
    message_backend_path = consumer_conf['MESSAGE_BACKEND_CONF'].get('API_PATH', None)
    backend_service_conf = consumer_conf['MESSAGE_BACKEND_CONF'].get('BACKEND_SERVICE_CONF', None)
    broker_service_conf = consumer_conf['MESSAGE_BROKER_CONF'].get('BROKER_SERVICE_CONF', None)
    broker_service_username = consumer_conf['MESSAGE_BROKER_CONF'].get('USER_NAME', None)
    broker_service_password = consumer_conf['MESSAGE_BROKER_CONF'].get('PASSWORD', None)
    broker_service_addr = consul_service(broker_service_conf)

    broker_conf = 'amqp'+"://"+broker_service_username+":"+broker_service_password+'@'+broker_service_addr
    if message_backend_path:
        backend_service_addr = consul_service(backend_service_conf)
        consumer = RabbitMQConsumer(
            queue=queue_conf.get('QUEUE', None),
            message_broker=broker_conf,
            message_backend="http://{}{}".format(backend_service_addr, message_backend_path)
        )
    else:
        consumer = RabbitMQConsumer(
            queue=queue_conf.get('QUEUE', None),
            message_broker=broker_conf,
            message_backend=message_backend_path)
    consumer.target_func_map = queue_conf.get('TARGET_FUNC_MAP', None)
    consumer.consume()
