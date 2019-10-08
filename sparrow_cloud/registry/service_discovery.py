import os
import consul
import logging
from random import randint
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from requests.exceptions import ConnectionError

logger = logging.getLogger(__name__)


def get_settings_value(name):
    """获取settings中的配置"""
    value = getattr(settings, name, None)
    if value == '' or value is None:
        raise NotImplementedError("没有配置这个参数%s" % name)
    return value


def _build_env_host_name(NAME):
    ENV_SERVICE_HOST_KEY = NAME + "_HOST"
    env_service_host = os.environ.get(ENV_SERVICE_HOST_KEY, "")
    return env_service_host


def consul_service(service_conf):
    """
    从consul service 拿到服务配置
    "SERVICE_CONF": {
        "ENV_NAME": "PERMISSION_REGISTER_NAME_HOST",
        "VALUE": "sprrow-permission-svc"
    }
    ENV_NAME: 用来覆盖 consul 的环境变量名
    VALUE: consul服务注册名字
    """
    # 获取 _HOST 对应的环境变量是否存在

    name = service_conf['ENV_NAME']
    env_service_host = os.environ.get(name, "")
    if env_service_host:
        # 获取对应的环境变量, 如果环境变量存在, 返回对应的环境变量
        return env_service_host
    else:
        # 对应的环境变量不存在, 使用服务发现
        consul_conf = get_settings_value('CONSUL_CLIENT_ADDR')
        consul_host = consul_conf.get('HOST', None)
        consul_port = consul_conf.get('PORT', None)
        service_register_name = service_conf['VALUE']
        if service_register_name:
            if (consul_host and consul_port) is None:
                raise NotImplementedError("CONSUL_CLIENT_ADDR:consul_host={},consul_port={},必须同时配置")
            consul_client = consul.Consul(host=consul_host, port=consul_port, scheme="http")
            try:
                consul_data = consul_client.catalog.service(service_register_name)[1]
                index = get_loadbalance_index(len(consul_data))
                port = consul_data[index]['ServicePort']
                address = consul_data[index]['ServiceAddress']
                domain = "{address}:{port}".format(address=address, port=port)
            except ConnectionError:
                raise ConnectionError('consul服务无法连接， 请检查配置')
            except ValueError:
                raise ImproperlyConfigured('consul中不存在：{}， 请检查服务名称是否正确'.format(service_conf['VALUE']))
            return domain
        else:
            raise ImproperlyConfigured('请检查配置：SERVICE_CONF，ENV_NAME和VALUE必须配置一个。')


def get_loadbalance_index(value):
    """返回一个0， value 之间的随机数， consul负载均衡使用"""
    return randint(0, int(value)-1)
