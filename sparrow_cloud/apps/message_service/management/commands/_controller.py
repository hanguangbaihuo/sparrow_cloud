# -*- coding: utf-8 -*-
from pika.exceptions import AMQPConnectionError as BrokerConnectonException
from datetime import datetime
from sparrow_cloud.restclient import rest_client

import base64, decimal, collections
import importlib
import json
import logging
import os
import pika
import time
import requests
import importlib
import functools
import threading

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='rabbitmq_consumer.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)
logger = logging.getLogger(__name__)


class PythonObjectEncoder(json.JSONEncoder):
    def default(self, o):
        if type(o) in (datetime.datetime, decimal.Decimal):
            return str(o)
        if isinstance(o, collections.Set):
            return list(o)
        else:
            return super(PythonObjectEncoder, self).default(o)


class RabbitMQConsumer(object):
    """
    rabitmq消费者
    """

    def __init__(self, queue, message_broker_conf, message_backend_svc=None, message_backend_api=None,
                retry_times=3, interval_time=3, heartbeat=60):
        """
        输入参数说明：
        queue:  定义consumer所在队列
        message_broker_conf: rabbitmq连接设置
        message_backend_conf: 选填的配置，如果设置了message_backend_conf,则在任务执行完成之后会向该设置里的url发送任务执行完成结果
        """
        # 检查queue的定义，已经queue是否已经存在在broker中
        
        if not message_broker_conf:
            raise Exception("message_broker not defined")
        self._message_broker = message_broker_conf
    
        if not queue:
            raise Exception("queue is not defined")
        self._queue = queue

        self._message_backend_svc = message_backend_svc
        self._message_backend_api = message_backend_api
        self._retry_times = retry_times
        self._interval_time = interval_time
        self._heartbeat = heartbeat

        # 最终执行任务的函数
        self._target_func_map = None
        self._channel = None

    @functools.lru_cache(maxsize=None)
    def get_target_func(self, func_name):
        # print("==========调用get_target_func, func_name={}".format(func_name))
        try:
            module_path, cls_name = func_name.rsplit(".", 1)
            func = getattr(importlib.import_module(module_path), cls_name)
        except Exception as ex:
            error = "error happened when setting target_func_map, {}".format(ex.__str__())
            logger.error(error)
            raise Exception(error)
        return func

    def _get_target_func_map(self):
        return self._target_func_map

    def _set_target_func_map(self, target_func_map):
        for func in target_func_map.values():
            self.get_target_func(func)

        self._target_func_map = target_func_map

    target_func_map = property(_get_target_func_map, _set_target_func_map)

    def ack_message(self, channel, delivery_tag):
        """Note that `channel` must be the same pika channel instance via which
        the message being ACKed was retrieved (AMQP protocol constraint).
        """
        if channel.is_open:
            channel.basic_ack(delivery_tag)
        else:
            # Channel is already closed, so we can't ACK this message;
            logger.error(
                'channel is closed, delivery_tag {0} cannot be ACKed'.format(delivery_tag))

    def set_parent_options(self, task_id, task_name):
        """
        设定父任务环境变量
        """
        parent_options = {
                "id": task_id,
                "code": task_name
        }
        try:
            os.environ["SPARROW_TASK_PARENT_OPTIONS"] = json.dumps(parent_options, cls=PythonObjectEncoder)
        except:
            pass
        return parent_options

    def base64_to_json(self, body):
        """
        base64编码的body 转成字符串
        """
        my_json = base64.b64decode(body).decode('utf8')
        json_data = json.loads(my_json)
        return json_data

    def get_task_info(self, headers, body):
        """
        从消息头和消息体中提取消息
        """
        delivery_info = headers.get('delivery_info', {})
        parent_options = headers.get('parent_options', {})
        json_body = self.base64_to_json(body)

        # 提取消息
        task_info = {
                "id": headers.get("task_id"), # from headers
                "name": json_body.get("name"), # from body.name 
                "task_args": json.dumps(json_body.get("args"), cls=PythonObjectEncoder), # from body.args
                "task_kwargs": json.dumps(json_body.get("kwargs"), cls=PythonObjectEncoder), # from body.kwargs
                "origin": headers.get('origin'), # from headers
                "created_time": delivery_info.get('created_time', None), # from headers
                "exchange": delivery_info.get('exchange', None), # from headers
                "routing_key": delivery_info.get('routing_key', None), # from headers 
                # "detail": str({'body': body, 'properties': header_frame}), 重新投递未使用到此字段
                "is_sent": True,
                "parent_id": parent_options.get('id', None), # from env 
                "parent_code": parent_options.get('code', None), # from env
      
        }
        return json.dumps(task_info, cls=PythonObjectEncoder)

    def do_work(self, connection, channel, method_frame, header_frame, body):

        thread_id = threading.get_ident()
        delivery_tag = method_frame.delivery_tag
        headers = header_frame.headers
        task_id = headers.get("task_id")

        fmt1 = 'Thread id: {} Delivery tag: {} Message body: {} Message Header: {} Task_id:{}'
        logger.info(fmt1.format(thread_id, delivery_tag, body, headers, task_id))

        logger.info(
            ' [*] {0} Received task_id {1}. Executing...'.format(datetime.now(), task_id))

        consumer = "unknown"
        try:
            # import pdb; pdb.set_trace()
            # consumer = method_frame.consumer_tag
            # consumer放执行消息的队列
            consumer = self._queue
            json_body = self.base64_to_json(body)

            task_name = json_body.get('name')
            task_args = json_body.get('args')
            task_kwargs = json_body.get('kwargs')
            # 设定父任务环境变量，以防下次发送子任务的时候需要用到
            self.set_parent_options(task_id, task_name)
            
            # 执行消费函数
            result = self.get_target_func(self.target_func_map[task_name])(*task_args, **task_kwargs)
            try:
                json_result = json.dumps(result, cls=PythonObjectEncoder)
            except:
                json_result = str(result) if result else ''
            if json_result == 'false':
                kwargs = {
                    "status": "FAILURE",
                    "result": json_result,
                    "traceback": ""
                }
            else:
                kwargs = {
                    "status": "SUCCESS",
                    "result": json_result,
                    "traceback": "",
                }
        except Exception as ex:
            kwargs = {
                "status": "FAILURE",
                "result": "",
                "traceback": ex.__str__()
            }
        try:
            # 提取完整消息
            task_info = self.get_task_info(headers, body)
            kwargs["task_info"] = task_info
            self.update_task_result(task_id, consumer, **kwargs)
        except Exception as ex:
            # sparrow_task服务重启的过程中，可能会遇到连接失败的情况以及提取消息失败
            # 所以需要忽略错误，不能影响consumer正常消费以及ack消息
            fm2 = "Task_id:{} update_task_result error:{}  ".format(task_id, ex.__str__())
            logger.error(fm2)
        logger.info(
            ' [*] {0} Finished task_id {1}.'.format(datetime.now(), task_id))

        cb = functools.partial(self.ack_message, channel, delivery_tag)
        connection.add_callback_threadsafe(cb)

    def on_message(self, channel, method_frame, header_frame, body, args):
        (connection, threads) = args
        t = threading.Thread(target=self.do_work, args=(
            connection, channel, method_frame, header_frame, body))
        t.start()
        threads.append(t)

    def consume(self):
        # logger.info(' [*] QUEUE({}) Waiting for messages. To exit press CTRL+C'.format(self._queue))
        # # 建立连接
        # while循环放在外面，因为如果出现网络连接错误，有可能是服务地址发生改变
        # while True: 
        try:
            # import pdb; pdb.set_trace()
            # parameters = pika.URLParameters("{0}?heartbeat={1}".format(self._message_broker, self._heartbeat))
            host = self._message_broker['host']
            port = self._message_broker['port']
            username = self._message_broker['username']
            password = self._message_broker['password']
            virtual_host = self._message_broker['virtual_host']
            credentials = pika.PlainCredentials(username, password, erase_on_connect=True)
            connection_parameters = pika.ConnectionParameters(host,
                                                        port,
                                                        virtual_host,
                                                        credentials,
                                                        heartbeat=self._heartbeat)

            connection = pika.BlockingConnection(connection_parameters)
            self._channel = connection.channel()
            logger.info(
                ' [*] QUEUE({0}) Waiting for messages. To exit press CTRL+C'.format(self._queue))
            self._channel.basic_qos(prefetch_count=1)
            threads = []
            on_message_callback = functools.partial(
                self.on_message, args=(connection, threads))
            self._channel.basic_consume(
                queue=self._queue, on_message_callback=on_message_callback)
            self._channel.start_consuming()

            for thread in threads:
                thread.join()
        # connection was closed by broker
        except pika.exceptions.ConnectionClosedByBroker:
            if self._channel:
                self._channel.stop_consuming()
            error_message = "pika.exceptions.ConnectionClosedByBroker. try again later"
            logger.error(error_message)
            raise Exception(error_message)
        except pika.exceptions.AMQPChannelError:
            if self._channel:
                self._channel.stop_consuming()
            error_message = "pika.exceptions.AMQPChannelError. try again later"
            logger.error(error_message)
            raise Exception(error_message)
        except BrokerConnectonException as ex:
            error_message = "broker connection error:{0}. try again later".format(ex.__repr__())
            logger.error(error_message)
            raise Exception(error_message)
        except Exception as ex:
            error_message = "rabbitmq consumer接收到异常，错误消息为{0}".format(ex.__str__())
            logger.error(error_message)
            raise Exception(error_message)

    def update_task_result(self, task_id, consumer, **kwargs):
        # 如果出现消息结果更新失败的情况，需要等待interval_time时间间隔来重试
        interval_time = self._interval_time
        error_message = None
        for _ in range(self._retry_times):
            try:
                status = kwargs.get('status')
                data = {
                    "task_id": task_id,
                    "consumer": consumer,
                    "status": status,
                    "result": kwargs.get('result'),
                    "traceback": kwargs.get('traceback'),
                    "task_info":kwargs.get('task_info'),
                }
                # sparrow_task服务重启的过程中，可能会遇到连接失败的情况
                response = rest_client.post(self._message_backend_svc, api_path=self._message_backend_api, json=data)
                logger.info(
                    ' [*] Update task database info task_id is {0}, status is {1}'.format(task_id, status))
                return
            except Exception as ex:
                time.sleep(interval_time)
                interval_time += 2
                error_message = ex.__str__()
        raise Exception("消息执行结果更新失败，消息id={}, 失败原因={},重试次数={}，消息执行状态={}，result={}, traceback={}".format(
                        task_id, error_message, self._retry_times, status, kwargs.get('result'), kwargs.get('traceback')))
            