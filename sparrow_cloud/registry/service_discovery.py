# import os
# import consul
# import logging
# from random import randint
# from django.conf import settings
# from django.core.exceptions import ImproperlyConfigured
# from requests.exceptions import ConnectionError
#
# logger = logging.getLogger(__name__)
#
#
# def get_settings_value(name):
#     """获取settings中的配置"""
#     value = getattr(settings, name, None)
#     if value == '' or value is None:
#         raise NotImplementedError("没有配置这个参数%s" % name)
#     return value
#
#
# def _build_env_host_name(NAME):
#     ENV_SERVICE_HOST_KEY = NAME + "_HOST"
#     env_service_host = os.environ.get(ENV_SERVICE_HOST_KEY, "")
#     return env_service_host
#
#
# def consul_address(service_conf):
#     """return: consul address list"""
#     env_name = service_conf.get("ENV_NAME", None)
#     if env_name:
#         env_service_host = os.environ.get(env_name, "")
#         if env_service_host != '':
#             # 获取对应的环境变量, 如果环境变量存在, 返回对应的环境变量
#             return env_service_host
#         else:
#             consul_conf = get_settings_value('CONSUL_CLIENT_ADDR')
#             consul_host = consul_conf.get('HOST', None)
#             consul_port = consul_conf.get('PORT', None)
#             service_register_name = service_conf.get("VALUE", None)
#             if service_register_name:
#                 if (consul_host and consul_port) is None:
#                     raise NotImplementedError("CONSUL_CLIENT_ADDR:consul_host={},consul_port={},必须同时配置")
#                 consul_client = consul.Consul(host=consul_host, port=consul_port, scheme="http")
#                 try:
#                     consul_address_list = consul_client.catalog.service(service_register_name)[1]
#                 except ConnectionError:
#                     raise ConnectionError('consul服务无法连接， 请检查配置')
#                 return consul_address_list
#             else:
#                 raise ImproperlyConfigured('请检查配置：SERVICE_CONF，ENV_NAME和VALUE必须配置一个。')
#
#
# def load_balance_address(address_list):
#     """return: 0， value 之间的随机数， consul负载均衡使用"""
#     if address_list:
#         index = randint(0, len(address_list)-1)
#         return address_list[index]
#     else:
#         raise ValueError("ValueError")
#
#
# def consul_service(service_conf):
#     """
#     "SERVICE_CONF": {
#         "ENV_NAME": "PERMISSION_REGISTER_NAME_HOST",
#         "VALUE": "sprrow-permission-svc"
#     }
#     ENV_NAME: 用来覆盖 consul 的环境变量名
#     VALUE: consul服务注册名字
#     """
#     # 获取 _HOST 对应的环境变量是否存在
#     name = service_conf['ENV_NAME']
#     env_service_host = os.environ.get(name, "")
#     if env_service_host:
#         # 获取对应的环境变量, 如果环境变量存在, 返回对应的环境变量
#         return env_service_host
#     consul_address_list = consul_address(service_conf)
#     try:
#         address = load_balance_address(consul_address_list)
#     except ValueError:
#         raise ImproperlyConfigured('请检查服务是否在consul中注册，service_name:{}'.format(service_conf['VALUE']))
#     host = address['ServiceAddress']
#     port = address['ServicePort']
#     domain = "{host}:{port}".format(host=host, port=port)
#     return domain
