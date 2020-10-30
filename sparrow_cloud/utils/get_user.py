# -*- coding: utf-8 -*-
from sparrow_cloud.utils.get_settings_value import get_settings_value
from sparrow_cloud.utils.common_exceptions import AuthenticationValidError

import importlib
import functools

SPARROW_AUTHENTICATION = 'SPARROW_AUTHENTICATION'
USER_CLASS_PATH = 'USER_CLASS_PATH'


def get_user_class_path():
    """Get the data in settings and add value validation"""
    sparrow_authentication = get_settings_value("SPARROW_AUTHENTICATION")
    return sparrow_authentication["USER_CLASS_PATH"]


@functools.lru_cache(maxsize=None)
def get_user_class():
    user_class_path = get_user_class_path()
    module_path, cls_name = user_class_path.rsplit(".", 1)
    try:
        user_cls = getattr(importlib.import_module(module_path), cls_name)
    except Exception as ex:
        raise AuthenticationValidError('UserIDAuthentication ERROR: USER_CLASS_PATH ，MESSAGE:{}'.format(str(ex)))
    return user_cls
