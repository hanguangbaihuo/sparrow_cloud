import unittest
from unittest import mock
from sparrow_cloud.registry.service_registry import consul_service


def mock_get_settings_value(name):
    """获取settings中的配置"""
    service_conf = {
        "host": "127.0.0.1",
        "port": 8500
    }
    return service_conf


class MockDjangoCache(object):

    @classmethod
    def get(cls, key):
        mock_data = {
            "service": "127.0.0.1:8001"
        }
        return mock_data

    @classmethod
    def set(cls, key, data, timeout):
        pass


SERVICE = {
    "service_name": "service",
    "host": "127.0.0.1:8001"
}


SERVICE1 = {
    "service_name": "service",
    "host": ""
}


class ConsulService(unittest.TestCase):

    @mock.patch('sparrow_cloud.registry.service_registry.get_settings_value', side_effect=mock_get_settings_value)
    def test_consul_parameter_host(self, get_settings_value):
        """测试参数中带host参数"""
        addr = consul_service(SERVICE)
        self.assertEqual(addr, '127.0.0.1:8001')
#     #
#     # @mock.patch('django.core.cache.cache', side_effect=MockDjangoCache)
#     # @mock.patch('sparrow_cloud.registry.service_registry.get_settings_value', side_effect=mock_get_settings_value)
#     # def test_consul_no_parameter_host(self, get_settings_value, cache):
#     #     """测试无host参数，从cache中拿服务地址"""
#     #     import pdb;pdb.set_trace()
#     #     addr = consul_service(SERVICE1)
#     #     self.assertEqual(addr, '127.0.0.1:8001')



