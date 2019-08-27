from django.core.management.base import BaseCommand


from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from rest_framework.settings import api_settings
from drf_yasg.codecs import OpenAPICodecJson, OpenAPICodecYaml
import json
import re


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        api_version = api_settings.DEFAULT_VERSION
        api_url = swagger_settings.DEFAULT_API_URL
        api_info = openapi.Info(title='111', default_version='v1')
        generator_class = swagger_settings.DEFAULT_GENERATOR_CLASS
        generator = generator_class(info=api_info, version=api_version, url=api_url)
        request = None
        public = True
        schema = generator.get_schema(request=request, public=public)
        # print(schema)
        codec = OpenAPICodecJson(validators=[], pretty=True)
        swagger_json = codec.encode(schema).decode('utf-8')
        # import pdb; pdb.set_trace()
        print(swagger_json)
        data = json.loads(swagger_json)
        _basepath = data['basePath']
        _path = data['paths']
        _keys = _path.keys()
        _schema_paths = []
        basepath_len = len(_basepath)
        # pattern = re.compile('\{.*\}')
        # 匹配任意 {} 之前的内容, 包含{}, 但该内容不包含 \
        pattern = re.compile('\{((?!\/).)*\}')
        for one in _keys:
            _schema_paths.append(_basepath + one)
        # import pdb; pdb.set_trace()
        print(_schema_paths)
        regx_list = []
        for _key in _schema_paths:
            _perm = _key[basepath_len:]
            _methods = _path[_perm].keys()
            for one in _methods:
                if one != "parameters":
                    path = _key
                    methods = one.upper()
                    pathregx = "^"+pattern.sub('[^/]*', _key)+"$"
                    regx_list.append(pathregx)
                    print("path=%s, method=%s, regx=%s" % (path, methods, pathregx))
        print(regx_list)
        regx_list = [re.compile(pa) for pa in regx_list]
        path = "/api/testapp/zz/asef/ddd/asef/"
        for pa in regx_list:
            xx = re.search(pa, path)
            print(xx)
