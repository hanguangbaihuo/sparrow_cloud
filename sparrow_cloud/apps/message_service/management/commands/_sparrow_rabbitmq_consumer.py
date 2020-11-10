from ._controller import RabbitMQConsumer
from sparrow_cloud.apps.message_service.aliyun_amqp import AliyunCredentialsProvider3 as aliyun_provider
from sparrow_cloud.utils.get_cm_value import get_cm_value
from sparrow_cloud.utils.get_settings_value import get_settings_value
import time


def rabbitmq_consumer(queue):
    """
    SparrowRabbitmpConsumer

        参数：
            queue # settings里面queue_conf 配置

        configmap 配置：
            SC_BROKER_USERNAME: 用户名
            SC_BROKER_PASSWORD: 密码
            SC_BROKER_VIRTUAL_HOST: VIRTUAL_HOST
            SC_BROKER_SERVICE_SVC: 依赖服务
            SC_BACKEND_SERVICE_SVC: 依赖服务
            SC_BACKEND_SERVICE_API: api
            SC_CONSUMER_RETRY_TIMES: 错误重试次数，默认3次
            SC_CONSUMER_INTERVAL_TIME: 错误重试间隔，默认3秒
            SC_CONSUMER_HEARTBEAT: 消费者与rabbitmq心跳检测间隔，默认600秒

        QUEUE_CONF_1 = {
            "QUEUE": "ORDER_PAY_SUC_ALL",
            "TARGET_FUNC_MAP": {
                "ORDER_PAY_SUC_ONLINE": ""
            }
        }
        ps: 
            QUEUE_CONF_1  # 队列的配置
            QUEUE  # 队列名称
            TARGET_FUNC_MAP  # 队列消费的任务（字典中的键为message code，
                                对应的值为执行该消息的任务函数路径字符串）

    """
    queue_conf = get_settings_value(queue)
    retry_times = get_cm_value('SC_CONSUMER_RETRY_TIMES')
    interval_time = get_cm_value('SC_CONSUMER_INTERVAL_TIME')
    consumer_heartbeat = get_cm_value('SC_CONSUMER_HEARTBEAT')

    virtual_host = get_cm_value("SC_BROKER_VIRTUAL_HOST")
    host = get_cm_value("SC_BROKER_SERVICE_HOST")
    port = get_cm_value("SC_BROKER_SERVICE_PORT")
    username = get_cm_value("SC_BROKER_USERNAME")
    password = get_cm_value('SC_BROKER_PASSWORD')
    backend_service_svc = get_cm_value('SC_BACKEND_SERVICE_SVC')
    backend_service_api = get_cm_value('SC_BACKEND_SERVICE_API')
    message_broker_conf = {
        "host": host,
        "port": port,
        "username": username,
        "password": password,
        "virtual_host": virtual_host,
        }
    while True:
        try:
            consumer = RabbitMQConsumer(
                queue=queue_conf.get('QUEUE', None),
                message_broker_conf=message_broker_conf,
                message_backend_svc=backend_service_svc,
                message_backend_api=backend_service_api,
                retry_times=int(retry_times),
                interval_time=int(interval_time),
                heartbeat=int(consumer_heartbeat)
            )
            consumer.target_func_map = queue_conf.get('TARGET_FUNC_MAP', None)
            consumer.consume()
        except KeyboardInterrupt:
            break
        except:
            # 如果遇到exception不退出，过几秒重试一下
            time.sleep(int(interval_time))
