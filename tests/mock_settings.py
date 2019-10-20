# -*- coding: utf-8 -*-


SECRET_KEY = "ss"

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

REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_L10N = True

USE_TZ = False
