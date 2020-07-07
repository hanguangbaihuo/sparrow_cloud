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
    'sparrow_cloud.apps.access_control'
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


SERVICE_CONF = {
    "NAME": "sparrow_cloud",
    "SECRET": "124cdsalhdisahgisabjnjlk"
}

REGISTRY_APP_CONF = {
        "SERVICE_ADDRESS": "sparrow-service-svc:8000",
        "PATH": "/api/get_app_token/",
        "ENABLE_TOKEN_CACHE": os.environ.get("ENABLE_TOKEN_CACHE", False)
    }