# import consul
# import json
# import datetime
# from django.core.cache import cache
# from django.conf import settings
# from requests.exceptions import ConnectionError
#
#
# def get_settings_value(name, prompt):
#     """获取settings中的配置"""
#     value = getattr(settings, name, None)
#     if value == '' or value is None:
#         raise NotImplementedError("{}:{}".format(prompt, name))
#     return value
#
#
# def config(key):
#     """
#     返回consul或settings的配置信息
#     优先级顺序：consul --> settings
#         consul中优先级顺序
#             consul正常：consul --> redis(30内有效期内)
#             consul异常：如果数据存在 redis， 直接返回
#     :param key:
#     :return:
#     """
#     consul_conf = get_settings_value(name='CONSUL_CLIENT_ADDR', prompt="没有配置这个参数")
#     consul_host = consul_conf.get('HOST', None)
#     consul_port = consul_conf.get('PORT', None)
#     if (consul_host and consul_port) is None or (consul_host and consul_port) == '':
#         raise NotImplementedError("CONSUL_CLIENT_ADDR:consul_host,consul_port,必须同时配置")
#     cache_value = get_cache_key(key)
#     if cache_value:
#         return cache_value
#     try:
#         consul_client = consul.Consul(host=consul_host, port=consul_port, scheme="http")
#         index, data = consul_client.kv.get(key, index=None)
#         if data:
#             value = json.loads(data.get('Value'))
#             value['cache_time'] = datetime.datetime.now()
#             cache.set(key, value, 7*24*3600)
#             value.pop('cache_time')
#             return value
#     except ConnectionError:
#         cache_value = cache.get(key)
#         if cache_value:
#             cache_value.pop('cache_time')
#             return cache_value
#         value = get_settings_value(name=key, prompt="配置中心和项目 settings 均无此参数")
#         return value
#
#
# def get_cache_key(key):
#     """获取缓存时间30秒内的数据"""
#     cache_value = cache.get(key)
#     if cache_value:
#         cache_time = cache_value.get('cache_time')
#         current_time = datetime.datetime.now()
#         if int((current_time - cache_time).seconds) <= 30:
#             cache_value.pop('cache_time')
#             return cache_value
#     return ''
