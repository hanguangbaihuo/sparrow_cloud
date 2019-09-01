import logging
import consul
from django.core.cache import cache
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)


def get_settings_value(name):
    """获取settings中的配置"""
    value = getattr(settings, name, None)
    if value == '' or value is None:
        raise NotImplementedError("没有配置这个参数%s" % name)
    return value


def consul_service(service_conf):
    """从consul service 拿到服务的名称"""
    consul_conf = get_settings_value('CONSUL_CLIENT_ADDR')
    consul_host = consul_conf.get('HOST', None)
    consul_port = consul_conf.get('PORT', None)
    service_name = service_conf.get('NAME_SVC', None)
    service_host = service_conf.get('HOST', None)
    if service_host:
        return service_host
    if service_name:
        service_cache = cache.get(service_name)
        if service_cache:
            return service_cache
        if (consul_host and consul_port) is None:
            raise NotImplementedError("CONSUL_CLIENT_ADDR 参数不全，请检查settings中的参数配置")
        if consul_host and consul_port:
            consul_client = consul.Consul(host=consul_host,
                                          port=consul_port,
                                          scheme="http")
            try:
                port = consul_client.catalog.service(service_name)[1][0]['ServicePort']
                address = consul_client.catalog.service(service_name)[1][0]['ServiceAddress']
                domain = "{address}:{port}".format(address=address, port=port)
                cache.set(service_name, domain, timeout=30)
            except:
                raise ImproperlyConfigured(
                    'consul服务暂时不可用, 临时解决方法： 在service_conf中配置service_host')
            return domain
        else:
            raise ImproperlyConfigured(
                '参数不正确，请检查consul 配置是否争取或service_conf参数是否正确')
