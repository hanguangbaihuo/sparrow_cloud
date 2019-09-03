import unittest
from unittest import mock
from sparrow_cloud.registry.service_registry import consul_service


def mock_get_settings_value(name):
    """获取settings中的配置"""
    service_conf = {
        "HOST": "127.0.0.1",
        "PORT": 8500
    }
    return service_conf


SERVICE = {
    "SERVICE_REGISTER_NAME": "service",
    "HOST": "127.0.0.1:8001"
}

consul_data_list = [
    {'ServiceAddress': '162.23.7.247', 'ServicePort': 8001,},
    {'ServiceAddress': '142.27.4.252', 'ServicePort': 8001,},
    {'ServiceAddress': '122.21.8.131', 'ServicePort': 8001,},
]


class ConsulService(unittest.TestCase):

    @mock.patch('sparrow_cloud.registry.service_registry.get_settings_value', side_effect=mock_get_settings_value)
    def test_consul_parameter_host(self, get_settings_value):
        """测试参数中带host参数"""
        addr = consul_service(SERVICE)
        self.assertEqual(addr, '127.0.0.1:8001')

