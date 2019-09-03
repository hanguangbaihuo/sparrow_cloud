import unittest
from unittest import mock
from sparrow_cloud.registry.service_registry import consul_service


# def mock_get_settings_value(name):
#     """获取settings中的配置"""
#     service_conf = {
#         "HOST": "127.0.0.1",
#         "PORT": 8500
#     }
#     return service_conf

CONSUL_CONF = {
    "HOST": "127.0.0.1",
    "PORT": 8500
}


SERVICE_WITH_HOST_CONF = {
    "SERVICE_REGISTER_NAME": "service_svc",
    "HOST": "127.0.0.1:8001"
}

SERVICE_WITH_NO_HOST_CONF = {
    "SERVICE_REGISTER_NAME": "service_svc",
    "HOST": ""
}

CONSUL_RETURN_DATA = (
    "name", 
    [
        {'ServiceAddress': '162.23.7.247', 'ServicePort': 8001,},
        {'ServiceAddress': '142.27.4.252', 'ServicePort': 8001,},
        {'ServiceAddress': '122.21.8.131', 'ServicePort': 8001,},
    ]
)

class ConsulServiceTest(unittest.TestCase):

    @mock.patch('sparrow_cloud.registry.service_registry.get_settings_value', return_value=CONSUL_CONF)
    def test_consul_parameter_host(self, get_settings_value):
        """测试参数中带host参数"""
        addr = consul_service(SERVICE_WITH_HOST_CONF)
        self.assertEqual(addr, '127.0.0.1:8001')

    @mock.patch('consul.Consul.Catalog.service', return_value=CONSUL_RETURN_DATA)
    @mock.patch('sparrow_cloud.registry.service_registry.get_settings_value', return_value=CONSUL_CONF)
    def test_consul_parameter_no_host(self, mock_get_settings_value, mock_consul_service):
        """测试参数中不带host参数"""
        addr = consul_service(SERVICE_WITH_NO_HOST_CONF)
        expect_result_list = ['{}:{}'.format(ii["ServiceAddress"], ii['ServicePort']) for ii in CONSUL_RETURN_DATA[1]]
        self.assertEqual(addr in expect_result_list, True)

