from django.conf import settings


def get_settings_value(name):
    """get settings value"""
    value = getattr(settings, name, None)
    if value is None:
        raise NotImplementedError("sparrow_cloud error：settings not find:{}".format(name))
    return value


def get_service_name():
    """get service_name"""
    service_conf = getattr(settings, "SERVICE_CONF", None)
    if service_conf is None:
        raise NotImplementedError("sparrow_cloud error：settings not find:SERVICE_CONF")
    service_name = service_conf.get("NAME", None)
    if service_name is None:
        raise NotImplementedError("sparrow_cloud error：settings not find: SERVICE_CONF['NAME']")
    return service_name