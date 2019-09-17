# -*- coding: utf-8 -*-


SECRET_KEY = "ss"

INSTALLED_APPS = [
    "sparrow_cloud.apps.message_service",
    "sparrow_cloud.apps.permission_command",
    "sparrow_cloud.apps.table_api",
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
