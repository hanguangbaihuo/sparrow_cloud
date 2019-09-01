import re
from collections import defaultdict
from importlib import import_module
from django.conf import settings
from django.contrib.admindocs.views import simplify_regex
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
from django.utils import six
from django.utils.encoding import force_text, smart_text
from rest_framework import exceptions, serializers
from rest_framework.compat import coreapi, uritemplate, urlparse
from rest_framework.request import clone_request
from rest_framework.utils import formatting
from rest_framework.views import APIView
from pprint import pprint
import logging

logger = logging.getLogger(__name__)

'''
注册数据结构
{
    "service_name": "u",
    "api_list": [
        {
            "api_name": "api_name",
            "method": "GET",
            "path": "/api/ooo/",
            "origin_path": "/api/oooo/",
            "desc": "desc",
            "is_regex": "False"
        },
        {
            "api_name": "api_name",
            "method": "GET",
            "path": "/api/uuu/pppp/",
            "origin_path": "/api/odd/",
            "desc": "desc",
            "is_regex": "False"
        }
    ]
}
'''



header_regex = re.compile('^[a-zA-Z][0-9A-Za-z_]*:')

def common_path(paths):
    split_paths = [path.strip('/').split('/') for path in paths]
    s1 = min(split_paths)
    s2 = max(split_paths)
    common = s1
    for i, c in enumerate(s1):
        if c != s2[i]:
            common = s1[:i]
            break
    return '/' + '/'.join(common)

def as_query_fields(items):
    """
    Take a list of Fields and plain strings.
    Convert any pain strings into `location='query'` Field instances.
    """
    return [
        item if isinstance(item, coreapi.Field) else coreapi.Field(name=item, required=False, location='query')
        for item in items
    ]


def is_api_view(callback):
    """
    Return `True` if the given view callback is a REST framework view/viewset.
    """
    cls = getattr(callback, 'cls', None)
    return (cls is not None) and issubclass(cls, APIView)


def endpoint_ordering(endpoint):
    path, method, callback = endpoint
    method_priority = {
        'GET': 0,
        'POST': 1,
        'PUT': 2,
        'PATCH': 3,
        'DELETE': 4
    }.get(method, 5)
    return (path, method_priority)


class SchemaGenerator(object):
    default_mapping = {
        'get': 'read',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
    }
    known_actions = (
        'create', 'read', 'retrieve', 'list',
        'update', 'partial_update', 'destroy'
    )

    def __init__(self, name=None, version=None):
        self.init(title=name)

    def init(self, title=None, url=None, patterns=None, urlconf=None):
        assert coreapi, '`coreapi` must be installed for schema support.'

        if patterns is None and urlconf is not None:
            if isinstance(urlconf, six.string_types):
                urls = import_module(urlconf)
            else:
                urls = urlconf
            self.patterns = urls.urlpatterns
        elif patterns is None and urlconf is None:
            urls = import_module(settings.ROOT_URLCONF)
            self.patterns = urls.urlpatterns
        else:
            self.patterns = patterns

        if url and not url.endswith('/'):
            url += '/'

        self.title = title
        self.url = url
        self.endpoints = None

    def determine_path_prefix(self, paths):
        prefixes = []
        for path in paths:
            components = path.strip('/').split('/')
            initial_components = []
            for component in components:
                if '{' in component:
                    break
                initial_components.append(component)
            prefix = '/'.join(initial_components[:-1])
            if not prefix:
                # We can just break early in the case that there's at least
                # one URL that doesn't have a path prefix.
                return '/'
            prefixes.append('/' + prefix + '/')
        return common_path(prefixes)

    def _get_description_section(self, view, header, description):
        lines = [line for line in description.splitlines()]
        current_section = ''
        sections = {'': ''}

        for line in lines:
            if header_regex.match(line):
                current_section, seperator, lead = line.partition(':')
                sections[current_section] = lead.strip()
            else:
                sections[current_section] += '\n' + line


        if header in sections:
            return sections[header].strip()

        return sections[''].strip()

    def split_summary_from_description(self, description):
        """Decide if and how to split a summary out of the given description. The default implementation
        uses the first paragraph of the description as a summary if it is less than 120 characters long.
        :param description: the full description to be analyzed
        :return: summary and description
        :rtype: (str,str)
        """
        # https://www.python.org/dev/peps/pep-0257/#multi-line-docstrings
        summary = None
        summary_max_len = 120  # OpenAPI 2.0 spec says summary should be under 120 characters
        sections = description.split('\n', 1)
        if len(sections) == 2:
            sections[0] = sections[0].strip()
            if len(sections[0]) < summary_max_len:
                summary, description = sections
                description = description.strip()

        return summary, description[:1200]

    def get_register_api(self, top, components, request, public):
        '''
        按照注册中心的数据格式, 重新构建数据结构
        '''
        if not top:
            return None
        result = []
        for category in top:
            # import pdb; pdb.set_trace()
            endpoints=category['points']
            if endpoints is None or len(endpoints)==0:
                continue
            for path, (view_cls, methods) in sorted(endpoints.items()):
                for method, view in methods:
                    method_lower=method.lower()
                    method_name = getattr(view, 'action', method_lower)
                    method_docstring = getattr(view, method_name, None).__doc__
                    if method_docstring:
                        method_docstring = self._get_description_section(view, method.lower(),
                                                                         formatting.dedent(smart_text(method_docstring)))
                    else:
                        method_docstring = self._get_description_section(view, getattr(view, 'action', method.lower()),
                                                                         view.get_view_description())
                    if not method_docstring:
                        method_docstring = "_"
                    (name, desc) = self.split_summary_from_description(method_docstring)
                    if name is None:
                            name = desc
                    _path = {
                        "name": name,
                        # "path": path,
                        "method": method_lower,
                        "origin_path": path,
                        # "is_regex": False,
                        "desc": desc,
                        # "version": ""
                    }
                    result.append(_path)
        return result


    def handle_api_path(self, api_list):
        '''
        处理正则数据
        '''
        # path_pamas_pattern
        result = []
        pattern_param = re.compile('\{((?!\/).)*\}')
        pattern_str = '[^/]*'
        g = lambda pathregx: True if pattern_str in pathregx else False
        for api in api_list:
            origin_path = api['origin_path']
            regex_path = pattern_param.sub(pattern_str, origin_path)
            is_regex = g(regex_path)
            if is_regex:
                regex_path = "^" + regex_path + "$"

            method = api['method']
            desc = api["desc"]
            name = api["name"]

            regex_api = {
                "path": regex_path,
                "origin_path": origin_path,
                "method": method,
                "desc": desc[:500],
                "api_name": name[:30],
                "is_regex": is_regex,
            }
            result.append(regex_api)
            logger.info("path=%s, method=%s, regx=%s" % (origin_path, method, regex_path))
        return result

    def get_paths(self, top, components, request, public):
        """
        Generate the Swagger Paths for the API from the given endpoints.
        """
        if not top:
            return None

        ret=[]
        # import pdb; pdb.set_trace()
        for category in top:
            # print('~~~~~~~~~')

            endpoints=category['points']
            if endpoints is None or len(endpoints)==0:
                continue
            prefix = self.get_path(category['prefix'])
            if prefix.endswith("/"):
                prefix=prefix[0:-1]
            assert '{' not in prefix, "base path cannot be templated in swagger 2.0"

            paths = {}
            for path, (view_cls, methods) in sorted(endpoints.items()):
                _path={}
                #print(path)
                for method, view in methods:
                    # print(method)
                    # if not self.should_include_endpoint(path, method, view, public):
                    #     continue
                    method_lower=method.lower()
                    method_name = getattr(view, 'action', method_lower)
                    method_docstring = getattr(view, method_name, None).__doc__
                    if method_docstring:
                        method_docstring = self._get_description_section(view, method.lower(),
                                                                         formatting.dedent(smart_text(method_docstring)))
                    else:
                        method_docstring = self._get_description_section(view, getattr(view, 'action', method.lower()),
                                                                         view.get_view_description())
                    if not method_docstring:
                        method_docstring = "_"

                    (_name, _desc) = self.split_summary_from_description(method_docstring)
                    if _name is None:
                        _name = _desc
                    _path[method_lower]={"name": _name, "description": _desc}

                path_suffix = path[len(prefix):]
                if not path_suffix.startswith('/'):
                    path_suffix = '/' + path_suffix
                paths[path_suffix]=_path
            if not paths is None:
                ret.append({"basePath":prefix,"basePathArray":prefix.strip("/").split("/"),"paths":paths})
        #print(ret)
        return ret

    def get_schema(self, request=None,public=False):
        if self.endpoints is None:
            self.endpoints=[]
            self.get_api_endpoints(self.patterns,final_arrays=self.endpoints)
        ret=[]
        for group in self.endpoints:
            contents=group['points']
            prefix=group['prefix']
            view_cls = {}
            view_paths = defaultdict(list)
            for path, method,  callback in contents:
                view = callback.cls()
                _paths={}
                for attr, val in getattr(callback, 'initkwargs', {}).items():
                    setattr(view, attr, val)
                view.args = ()
                view.kwargs = {}
                view.format_kwarg = None

                actions = getattr(callback, 'actions', None)
                if actions is not None:
                    if method == 'OPTIONS':
                        view.action = 'metadata'
                    else:
                        view.action = actions.get(method.lower())

                if request is not None:
                    view.request = clone_request(request, method)
                    try:
                        view.check_permissions(view.request)
                    except exceptions.APIException:
                        continue
                else:
                    view.request = None
                view_paths[path].append((method, view))
                view_cls[path]=callback.cls
            ret.append({"prefix":group['prefix'],"points":{path: (view_cls[path], methods) for path, methods in view_paths.items()}})
        #print(len(ret))
        # return self.get_paths(ret, None, request, public=False)
        # return self.get_register_api(ret, None, request, public=False)
        register_api = self.get_register_api(ret, None, request, public=False)
        return self.handle_api_path(register_api)


    def get_api_endpoints(self, patterns, prefix='', final_arrays=[]):
        """
        Return a list of all available API endpoints by inspecting the URL conf.
        """
        api_endpoints = []

        for pattern in patterns:
            path_regex = prefix + pattern.regex.pattern
            if isinstance(pattern, RegexURLPattern):
                path = self.get_path(path_regex)
                callback = pattern.callback
                if self.should_include_endpoint(path, callback):
                    for method in self.get_allowed_methods(callback):
                        #action = self.get_action(path, method, callback)
                        #category = self.get_category(path, method, callback, action)
                        #endpoint = (path, method, category, action, callback)
                        endpoint = (path, method, callback)
                        api_endpoints.append(endpoint)

            elif isinstance(pattern, RegexURLResolver):
                self.get_api_endpoints(
                    patterns=pattern.url_patterns,
                    prefix=path_regex,
                    final_arrays=final_arrays
                )
                # api_endpoints.extend(nested_endpoints)
        if api_endpoints and len(api_endpoints)>0:
            api_endpoints = sorted(api_endpoints, key=endpoint_ordering)

            final_arrays.append({
                "prefix": prefix,
                "points": api_endpoints
            })
            # print('~~~~~~~%s'%len(final_arrays))
            # print(prefix)
            # print(api_endpoints)
            # print('@@@@@@@')
        return api_endpoints

    def get_path(self, path_regex):
        """
        Given a URL conf regex, return a URI template string.
        """
        path = simplify_regex(path_regex)
        path = path.replace('<', '{').replace('>', '}')
        return path

    def should_include_endpoint(self, path, callback):
        """
        Return `True` if the given endpoint should be included.
        """
        if not is_api_view(callback):
            return False  # Ignore anything except REST framework views.

        if path.endswith('.{format}') or path.endswith('.{format}/'):
            return False  # Ignore .json style URLs.

        if path == '/':
            return False  # Ignore the root endpoint.

        return True

    def get_allowed_methods(self, callback):
        """
        Return a list of the valid HTTP methods for this endpoint.
        """
        if hasattr(callback, 'actions'):
            return [method.upper() for method in callback.actions.keys()]

        return [
            method for method in
            callback.cls().allowed_methods if method not in ('OPTIONS', 'HEAD')
        ]

    def get_action(self, path, method, callback):
        """
        Return a descriptive action string for the endpoint, eg. 'list'.
        """
        actions = getattr(callback, 'actions', self.default_mapping)
        return actions[method.lower()]

    def get_category(self, path, method, callback, action):
        """
        Return a descriptive category string for the endpoint, eg. 'users'.
        Examples of category/action pairs that should be generated for various
        endpoints:
        /users/                     [users][list], [users][create]
        /users/{pk}/                [users][read], [users][update], [users][destroy]
        /users/enabled/             [users][enabled]  (custom action)
        /users/{pk}/star/           [users][star]     (custom action)
        /users/{pk}/groups/         [groups][list], [groups][create]
        /users/{pk}/groups/{pk}/    [groups][read], [groups][update], [groups][destroy]
        """
        path_components = path.strip('/').split('/')
        path_components = [
            component for component in path_components
            if '{' not in component
        ]
        if action in self.known_actions:
            # Default action, eg "/users/", "/users/{pk}/"
            idx = -1
        else:
            # Custom action, eg "/users/{pk}/activate/", "/users/active/"
            idx = -2

        try:
            return path_components[idx]
        except IndexError:
            return None

    # Methods for generating each individual `Link` instance...

    def get_link(self, path, method, callback, view):
        """
        Return a `coreapi.Link` instance for the given endpoint.
        """
        fields = self.get_path_fields(path, method, callback, view)
        fields += self.get_serializer_fields(path, method, callback, view)
        fields += self.get_pagination_fields(path, method, callback, view)
        fields += self.get_filter_fields(path, method, callback, view)

        if fields and any([field.location in ('form', 'body') for field in fields]):
            encoding = self.get_encoding(path, method, callback, view)
        else:
            encoding = None

        if self.url and path.startswith('/'):
            path = path[1:]

        return coreapi.Link(
            url=urlparse.urljoin(self.url, path),
            action=method.lower(),
            encoding=encoding,
            fields=fields
        )

    def get_encoding(self, path, method, callback, view):
        """
        Return the 'encoding' parameter to use for a given endpoint.
        """
        # Core API supports the following request encodings over HTTP...
        supported_media_types = set((
            'application/json',
            'application/x-www-form-urlencoded',
            'multipart/form-data',
        ))
        parser_classes = getattr(view, 'parser_classes', [])
        for parser_class in parser_classes:
            media_type = getattr(parser_class, 'media_type', None)
            if media_type in supported_media_types:
                return media_type
            # Raw binary uploads are supported with "application/octet-stream"
            if media_type == '*/*':
                return 'application/octet-stream'

        return None

    def get_path_fields(self, path, method, callback, view):
        """
        Return a list of `coreapi.Field` instances corresponding to any
        templated path variables.
        """
        fields = []

        for variable in uritemplate.variables(path):
            field = coreapi.Field(name=variable, location='path', required=True)
            fields.append(field)

        return fields

    def get_serializer_fields(self, path, method, callback, view):
        """
        Return a list of `coreapi.Field` instances corresponding to any
        request body input, as determined by the serializer class.
        """
        if method not in ('PUT', 'PATCH', 'POST'):
            return []

        if not hasattr(view, 'get_serializer'):
            return []

        serializer = view.get_serializer()

        if isinstance(serializer, serializers.ListSerializer):
            return [coreapi.Field(name='data', location='body', required=True)]

        if not isinstance(serializer, serializers.Serializer):
            return []

        fields = []
        for field in serializer.fields.values():
            if field.read_only or isinstance(field, serializers.HiddenField):
                continue

            required = field.required and method != 'PATCH'
            description = force_text(field.help_text) if field.help_text else ''
            field = coreapi.Field(
                name=field.source,
                location='form',
                required=required,
                description=description
            )
            fields.append(field)

        return fields

    def get_pagination_fields(self, path, method, callback, view):
        if method != 'GET':
            return []

        if hasattr(callback, 'actions') and ('list' not in callback.actions.values()):
            return []

        if not getattr(view, 'pagination_class', None):
            return []

        paginator = view.pagination_class()
        return as_query_fields(paginator.get_fields(view))

    def get_filter_fields(self, path, method, callback, view):
        if method != 'GET':
            return []

        if hasattr(callback, 'actions') and ('list' not in callback.actions.values()):
            return []

        if not hasattr(view, 'filter_backends'):
            return []

        fields = []
        for filter_backend in view.filter_backends:
            fields += as_query_fields(filter_backend().get_fields(view))
        return fields