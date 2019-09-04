import logging
import consul
from random import randint
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import os
logger = logging.getLogger(__name__)


def get_settings_value(name):
    """获取settings中的配置"""
    import pdb; pdb.set_trace()
    value = getattr(settings, name, None)
    if value == '' or value is None:
        raise NotImplementedError("没有配置这个参数%s" % name)
    return value

def _build_env_host_name(NAME):
    ENV_SERVICE_HOST_KEY = NAME + "_HOST"
    env_service_host = os.environ.get(ENV_SERVICE_HOST_KEY, "")
    return env_service_host

def consul_service(SERVICE_SETTINGS_KEY_NAME):
    """
    从consul service 拿到服务的名称
    SERVICE_SETTINGS_KEY_NAME: settings 里面的服务注册 key 值:
        例如:
            SPARROW_PERMISSION_REGISTER_NAME = "sparrow-permission-svc"
            服务调用方式:
                consul_service("SPARROW_PERMISSION_REGISTER_NAME")
    """
    # 获取 _HOST 对应的环境变量是否存在
    # import pdb; pdb.set_trace()
    env_service_host = _build_env_host_name(SERVICE_SETTINGS_KEY_NAME)
    if env_service_host:
        # 1 获取对应的环境变量, 如果环境变量存在, 返回对应的环境变量
        return env_service_host
    else:
        # 对应的环境变量不存在, 使用服务发现
        consul_conf = get_settings_value('CONSUL_CLIENT_ADDR')
        consul_host = consul_conf.get('HOST', None)
        consul_port = consul_conf.get('PORT', None)
        service_register_name = get_settings_value(SERVICE_SETTINGS_KEY_NAME)
        if service_register_name:
            if (consul_host and consul_port) is None:
                raise NotImplementedError("CONSUL_CLIENT_ADDR:consul_host={},consul_port={},必须同时配置")
            # if consul_host and consul_port:
            consul_client = consul.Consul(host=consul_host, port=consul_port, scheme="http")
            try:
                consul_data = consul_client.catalog.service(service_register_name)[1]
                index = get_loadbalance_index(len(consul_data))
                port = consul_data[index]['ServicePort']
                address = consul_data[index]['ServiceAddress']
                domain = "{address}:{port}".format(address=address, port=port)
            except:
                raise ImproperlyConfigured(
                    'consul服务暂时不可用, 临时解决方法： 在service_conf中配置service_host')
            return domain


def get_loadbalance_index(value):
    """返回一个0， value 之间的随机数， consul负载均衡使用"""
    return randint(0, int(value)-1)
