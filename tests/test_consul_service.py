import unittest
from unittest import mock
from django.conf import settings
from sparrow_cloud.registry.service_discovery import consul_service


# 与 SPARROW_SERVICE_REGISTER_NAME 对应的 _HOST
SPARROW_SERVICE_REGISTER_NAME_HOST = "127.0.0.1:8001"

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



# settings_mock = mock.Mock()
# settings_mock.SPARROW_SERVICE_REGISTER_NAME.return_value = "service_svc"
# settings_mock.CONSUL_CLIENT_ADDR.return_value = {
#     "HOST": "127.0.0.1",
#     "PORT": 8500
# }


class ConsulServiceTest(unittest.TestCase):

    @mock.patch.object('sparrow_cloud.registry.service_discovery.settings', mock_settings)
    def test_consul_parameter_host(self, mock_settings_func):
        """测试没有设置HOST 覆盖环境变量"""
        addr = consul_service("SPARROW_SERVICE_REGISTER_NAME")
        self.assertEqual(addr, '127.0.0.1:8001')

    # @mock.patch('consul.Consul.Catalog.service', return_value=CONSUL_RETURN_DATA)
    # @mock.patch('sparrow_cloud.registry.service_registry.get_settings_value', return_value=CONSUL_CLIENT_ADDR)
    # def test_consul_parameter_no_host(self, mock_get_settings_value, mock_consul_service):
    #     """测试参数中不带host参数"""
    #     addr = consul_service(SERVICE_WITH_NO_HOST_CONF)
    #     expect_result_list = ['{}:{}'.format(ii["ServiceAddress"], ii['ServicePort']) for ii in CONSUL_RETURN_DATA[1]]
    #     self.assertEqual(addr in expect_result_list, True)

