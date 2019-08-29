# -*- coding: utf-8 -*-
from sparrow_cloud.utils.get_settings_value import GetSettingsValue
from sparrow_django_common.utils.common_exceptions import AuthenticationValidError

import importlib
import functools

SPARROW_AUTHENTICATION = 'SPARROW_AUTHENTICATION'
USER_CLASS_PATH = 'USER_CLASS_PATH'


def get_settings_value():
    """Get the data in settings and add value validation"""
    settings_value = GetSettingsValue()
    user_class_path = settings_value.get_middleware_value(
        SPARROW_AUTHENTICATION, USER_CLASS_PATH)
    return user_class_path


@functools.lru_cache(maxsize=None)
def get_user_class():
    user_class_path = get_settings_value()
    module_path, cls_name = user_class_path.rsplit(".", 1)
    try:
        user_cls = getattr(importlib.import_module(module_path), cls_name)
    except Exception as ex:
        raise AuthenticationValidError('请检查settings下JWT_AUTHENTICATION_MIDDLEWARE中的USER_CLASS_PATH或'
                                       'USER_CLASS_PATH路径下的user是否正确')
    return user_cls
