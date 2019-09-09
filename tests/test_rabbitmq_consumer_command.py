import unittest
from unittest import mock
import django
from io import StringIO
from django.core.management import call_command
import os
from django.conf.urls import url
from django.http import HttpResponse


def task(*args, **kwargs):
    print('*'*10)


# SPARROW_RABBITMQ_CONSUMER_CONF = {
#
#     "MESSAGE_BROKER_CONF": {
#         "USER_NAME": "test_name",
#         "PASSWORD": "test_password",
#         "VIRTUAL_HOST": "test_virtual",
#         "BROKER_SERVICE_CONF": {
#             "ENV_NAME": "SPARROW_BROKER_HOST",
#             "VALUE": "sparrow-test",
#         },
#     },
#     "MESSAGE_BACKEND_CONF": {
#         "BACKEND_SERVICE_CONF": {
#             "ENV_NAME": "SPARROW_BACKEND_HOST",
#             "VALUE": "sparrow-demo",
#         },
#         "API_PATH": "/api/sparrow_test/task/test_update/"
#     }
# }


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


urlpatterns = [
    url(r'^/ssss/xxx/$', detail),
    url(r'^/ssuuu/xxddx/$', detail),
]


class RestClientTestCase(unittest.TestCase):

    def setUp(self):
        os.environ["SPARROW_BROKER_HOST"] = "127.0.0.1:8001"
        os.environ["SPARROW_BACKEND_HOST"] = "127.0.0.1:8002"
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"

    @mock.patch('rabbitmq_consumer.RabbitMQConsumer.target_func_map', return_value='')
    @mock.patch('rabbitmq_consumer.RabbitMQConsumer.consume', return_value='接收任务成功')
    def test_consumer_command(self, mock_target_func_map, mock_consume):
        from django.conf import settings
        self.setup_settings(settings)
        django.setup()
        out = StringIO()
        call_command('rabbitmq_consumer', '--queue', 'QUEUE_CONF', stdout=out)

    def setup_settings(self, settings):
        settings.XX = "1"
        settings.SECRET_KEY = "ss"
        settings.SPARROW_RABBITMQ_CONSUMER_CONF = {
                                "MESSAGE_BROKER_CONF": {
                                    "USER_NAME": "test_name",
                                    "PASSWORD": "test_password",
                                    "VIRTUAL_HOST": "test_virtual",
                                    "BROKER_SERVICE_CONF": {
                                        "ENV_NAME": "SPARROW_BROKER_HOST",
                                        "VALUE": "sparrow-test",
                                    },
                                },
                                "MESSAGE_BACKEND_CONF": {
                                    "BACKEND_SERVICE_CONF": {
                                        "ENV_NAME": "SPARROW_BACKEND_HOST",
                                        "VALUE": "sparrow-demo",
                                    },
                                    "API_PATH": "/api/sparrow_test/task/test_update/"
                                }
                            }

        settings.QUEUE_CONF={
            "QUEUE": "TEST_QUEUE",
            "TARGET_FUNC_MAP": {
                "ORDER_PAY_SUC_ONLINE": "./task",
            }
        }
        settings.ROOT_URLCONF = __name__
