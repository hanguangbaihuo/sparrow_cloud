# -*- coding: utf-8 -*-
import os

SECRET_KEY = "sssssssllllllllllllll"

INSTALLED_APPS = [
    "sparrow_cloud.apps.message_service",
    "sparrow_cloud.apps.permission_command",
    "sparrow_cloud.apps.table_api",
    "sparrow_cloud.apps.schema_command",
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

CONSUL_CLIENT_ADDR = {
    "HOST": os.environ.get("CONSUL_IP", "127.0.0.1"),
    "PORT": os.environ.get("CONSUL_PORT", 9999)
}

REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_L10N = True

USE_TZ = False


PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQDFaomEPnsKfzlzZXqFHPuhV4VeD+cIBCoHxSjhxwKRiERZ603T
AstuS56YEXTOKlMVbnZFuTdPEvhRZpiQNJDObpQ3ScPqgmXKs7WcdJ7PtMKoiBE0
q5wgB+lCqfDusAaCOcC2muBf+HMzo33D0NkO1K2quf2erSRTljzgJmwsowIDAQAB
AoGATnFjzSlqiKQ+9sx235fBoL1/H/4fpf7JmKbN9NC4A43q4vPty4/Lt7rSfMhK
6nTE6LoowtGy2XfHNckXjA1nD/0V+n/fWXDRWJ6JXHggvAPTzMIZqiaj4FZHoGKo
NdVwtIxFZBlSolMJ+fkW8d8gR6/hvpziJQ0EjzhAHBQHHfkCQQDhqgWHvqDjUWXx
Pj+44Jixg03TkyNSrlB8sjdqfRrcyIaq53p/XFEjC2GuqwBwqEHq/ZgFhCYaTQXh
5JMCW9iVAkEA3/RkkG0vRguo4JtzVEiC1z9PKjNVKoIixMERz9vex6qIZuhAnNxA
j22SKiK+6XRbx7V0lSWHF4TzJ/1OOxDKVwJAMotZd8Eb2i6GLdWqgidULBZj3SrM
s501i+iC/wgMdz025Jq6VkKALeBDvdKxY4pcUV0BquKhgiyUT7dZsiKOTQJBAN4a
Pv2o+uApwhL2t9rXisMzqyw7+nOM2jRtEWAmOvujmWENZr7qBDD6RqH5EYLvffJC
d9tOe3qMxKVdJo+XaEMCQDT1OCTBkR4RPqVLc+ZTr9zT4dPQzUJNIsyPuKKUM/f/
uG75zcd94ZeCO5ZyREP8/MHQvuzmUFxR96ePvEuxuwI=
-----END RSA PRIVATE KEY-----"""

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDFaomEPnsKfzlzZXqFHPuhV4Ve
D+cIBCoHxSjhxwKRiERZ603TAstuS56YEXTOKlMVbnZFuTdPEvhRZpiQNJDObpQ3
ScPqgmXKs7WcdJ7PtMKoiBE0q5wgB+lCqfDusAaCOcC2muBf+HMzo33D0NkO1K2q
uf2erSRTljzgJmwsowIDAQAB
-----END PUBLIC KEY-----"""


ACL_MIDDLEWARE = {
    "ACL_SERVICE": {
        # ENV_NAME 为覆盖consul的默认值, 环境变量名称示例：服务名称_HOST， 只需要给一个环境变量的NAME，不需要给VALUE
        "ENV_NAME": "SPARROW_SERVICE_ACL_HOST",
        # VALUE 为服务发现的注册名称
        "VALUE": os.environ.get("SPARROW_SERVICE_ACL_SVC", "acl_service"),
    },
    "API_PATH": "/api/acl_token/",
    "ACL_PUBLIC_KEY": PUBLIC_KEY
}