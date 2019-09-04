import unittest
from unittest import mock
from django.conf import settings
from sparrow_cloud.registry.service_discovery import consul_service

# 与 SPARROW_SERVICE_REGISTER_NAME 对应的 _HOST
SPARROW_SERVICE_REGISTER_NAME_HOST = "162.23.7.247:8001"

CONSUL_CONF = {
    "HOST": "127.0.0.1",
    "PORT": 8001
}

SPARROW_SERVICE_REGISTER_NAME = "sparrow"


CONSUL_RETURN_DATA = (
    "name", 
    [
        {'ServiceAddress': '162.23.7.247', 'ServicePort': 8001,},
        {'ServiceAddress': '142.27.4.252', 'ServicePort': 8001,},
        {'ServiceAddress': '122.21.8.131', 'ServicePort': 8001,},
    ]
)

def mock_settings():

    class MockSettings:
        SPARROW_SERVICE_REGISTER_NAME = "service_svc"
        CONSUL_CLIENT_ADDR = {
            "HOST": "127.0.0.1",
            "PORT": 8500
        }

    return MockSettings()
    

class ConsulServiceTest(unittest.TestCase):

    @mock.patch('consul.Consul.Catalog.service', return_value=CONSUL_RETURN_DATA)
    @mock.patch('sparrow_cloud.registry.service_discovery.get_settings_value', return_value=SPARROW_SERVICE_REGISTER_NAME)
    @mock.patch('sparrow_cloud.registry.service_discovery.get_settings_value', return_value=CONSUL_CONF)
    @mock.patch('sparrow_cloud.registry.service_discovery._build_env_host_name', return_value=SPARROW_SERVICE_REGISTER_NAME_HOST)
    def test_consul_parameter_variable(self, mock_host_name, mock_consul_conf, mock_service_register_name, mock_consul_service):
        """测试设置了环境变量"""   
        addr = consul_service("SPARROW_SERVICE_REGISTER_NAME")
        expect_result_list = ['{}:{}'.format(
            ii["ServiceAddress"], ii['ServicePort']) for ii in CONSUL_RETURN_DATA[1]]
        self.assertEqual(addr in expect_result_list, True)
