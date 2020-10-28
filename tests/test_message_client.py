import os
import unittest
from unittest import mock
from django.conf import settings


class TestMessage(unittest.TestCase):
    """test message client"""

    def setUp(self):
        pass
        # os.environ["SPARROW_TASK_TEST_SVC_HOST"] = "127.0.0.1:8001"
        # settings.MESSAGE_SENDER_CONF = {
        #     "SERVICE_CONF": "sparrow-task-test-svc:8001",
        #     "API_PATH": "/api/sparrow_task/producer/send/",
        # }
        # settings.TASK_PROXY_CONF = {
        #     "SERVICE_CONF": "sparrow-task-proxy-svc:8001",
        #     "API_PATH": "/api/sparrow_task_proxy/producer/send",
        # }

    @mock.patch('sparrow_cloud.message_service.sender.TaskSender.send_task', return_value={})
    def test_send_message(self, mock_send_task):
        from sparrow_cloud.message_service.sender import send_task
        exchange = 'topic_3'
        routing_key = 'order_pay_success'
        message_code = 'order_pay_success'
        data = send_task(exchange=exchange, routing_key=routing_key, message_code=message_code)
        self.assertEqual(data, {})


    @mock.patch('sparrow_cloud.message_service.sender.TaskSender.send_task', return_value={})
    def test_send_message_v2(self, mock_send_task):
        from sparrow_cloud.message_service.sender import send_task_v2
        message_code = 'order_pay_success'
        data = send_task_v2(message_code=message_code)
        self.assertEqual(data, {})

    @mock.patch('sparrow_cloud.message_service.sender.TaskSender.send_task', return_value={})
    def test_send_message_v3(self, mock_send_task):
        from sparrow_cloud.message_service.sender import send_task_v3
        message_code = 'order_pay_success'
        data = send_task_v3(message_code=message_code)
        self.assertEqual(data, {})
