from django.conf import settings


class GetSettingsValue(object):
    """settings数据"""

    def __get_settings_value(self, name):
        """获取settings中的配置， settings中数据"""
        value = getattr(settings, name, None)
        if value == '' or value is None:
            raise NotImplementedError("没有配置这个参数%s" % name)
        return value

    def __get_middleware_value(self, middleware_class, name):
        """
        获取中间件服务的配置数据,  PERMISSION_SERVICE 层数据，
        PERMISSION_MIDDLEWARE = {
            "PERMISSION_SERVICE":{
                "name": "",
                "host": "",
                "port": 8001,
                "address": "",
            },
            "CONSUL": {
                "host": "",
                "port": ,
                },
            "FILTER_PATH" : ['']
        }
        """
        service_value = self.__get_settings_value(middleware_class)
        value = service_value.get(name, None)
        if value == '' or value is None:
            raise NotImplementedError("没有配置这个参数%s" % name)
        return value

    def __get_middleware_service_value(self, middleware_class, service_name, key):
        """
        获取中间件中服务的具体配置的值, PERMISSION_SERVICE 下的 name 层数据
        PERMISSION_MIDDLEWARE = {
            "PERMISSION_SERVICE":{
                "name": "",
                "host": "",
                "port": 8001,
                "address": "",
            },
            "CONSUL": {
                "host": "",
                "port": ,
                },
            "FILTER_PATH" : ['']
        }
        """
        middleware_value = self.__get_middleware_value(middleware_class, service_name)
        value = middleware_value.get(key, None)
        if value == '' or value is None:
            raise NotImplementedError("没有配置这个参数%s" % service_name, key)
        return value

    def __get_middleware_value_not_validated(self, middleware_class, service_name, key):
        """获取middleware value 不验证value"""
        middleware_value = self.__get_middleware_value(middleware_class, service_name)
        value = middleware_value.get(key, None)
        if value is None:
            raise NotImplementedError("没有配置这个参数%s" % service_name, key)
        return value

    def __get_value(self, middleware_class, name):
        """
        获取中间件服务的配置数据,  PERMISSION_SERVICE 层数据， 不做任何验证
        PERMISSION_MIDDLEWARE = {
            "PERMISSION_SERVICE":{
                "name": "",
                "host": "",
                "port": 8001,
                "address": "",
            },
            "CONSUL": {
                "host": "",
                "port": ,
                },
            "FILTER_PATH" : ['']
        }
        """
        service_value = self.__get_settings_value(middleware_class)
        value = service_value.get(name, False)
        return value

    def get_settings_value(self, name):
        """获取settings中的服务配置"""
        value = self.__get_settings_value(name)
        return value

    def get_middleware_value(self, middleware_class, name):
        """获取中间件服务的值"""
        value = self.__get_middleware_value(middleware_class, name)
        return value

    def get_middleware_service_value(self, middleware_class, service_name, key):
        """获取settings具体的服务的具体配置的值"""
        value = self.__get_middleware_service_value(middleware_class, service_name, key)
        return value

    def get_middleware_value_not_validated(self, middleware_class, service_name, key):
        """获取settings中middleware不验证"""
        value = self.__get_middleware_value_not_validated(middleware_class, service_name, key)
        return value

    def get_value(self, middleware_class, name):
        """获取中间件服务的值"""
        value = self.__get_value(middleware_class, name)
        return value
