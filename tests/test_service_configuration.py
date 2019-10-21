import os
import datetime
import unittest
from unittest import mock
from django.core.cache import cache
from sparrow_cloud.registry.service_configuration import config



DATA = ('8018915', {'LockIndex': 0, 'Key': 'foo', 'Flags': 0, 'Value': b'{"test_key0":"value0",\n"test_key1":"value1"}',
                    'CreateIndex': 8018915, 'ModifyIndex': 8018915})


class ConsulServiceTest(unittest.TestCase):

    def setUp(self):
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"

    @mock.patch('consul.Consul.KV.get', return_value=DATA)
    def test_consul_parameter_variable(self, mock_consul_config_data):
        """
        测试从consul中取数据
        """
        from django.conf import settings
        settings.CONSUL_CLIENT_ADDR = {
            "HOST": "127.0.0.1",
            "PORT": 8500
        }
        data = config(key='foo')
        self.assertEqual("value0", data.get("test_key0"))
        self.assertEqual("value1", data.get("test_key1"))

    def test_consul_error(self):
        """
        测试cache value
        """
        from django.conf import settings
        data = {"test_key0": "value0", "test_key1": "value1"}
        data['cache_time'] = datetime.datetime.now()
        cache.set('foo', data, 60)
        settings.CONSUL_CLIENT_ADDR = {
            "HOST": "127.0.0.1",
            "PORT": "8500"
        }
        value = config(key='foo')
        self.assertEqual({"test_key0": "value0", "test_key1": "value1"}, value)

    @mock.patch('consul.Consul.KV.get', return_value=("", ""))
    def test_settings_value(self, mock_consul_data):
        """
        测试settings 数据
        """
        from django.conf import settings
        settings.foo = {"test_key0": "value0", "test_key1": "value1"}
        settings.CONSUL_CLIENT_ADDR = {
            "HOST": "127.0.0.1",
            "PORT": "8500"
        }
        value = config(key='foo')
        self.assertEqual({"test_key0": "value0", "test_key1": "value1"}, value)

    def tearDown(self):
        del os.environ["DJANGO_SETTINGS_MODULE"]
