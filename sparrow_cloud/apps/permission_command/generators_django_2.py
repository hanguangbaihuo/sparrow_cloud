import copy
import logging
import re
from django.conf import settings
from collections import OrderedDict, defaultdict
from rest_framework import versioning
from rest_framework.compat import URLPattern, URLResolver, get_original_route
from rest_framework.schemas.generators import EndpointEnumerator as _EndpointEnumerator
from rest_framework.schemas import SchemaGenerator
from rest_framework.schemas.generators import endpoint_ordering
from rest_framework.schemas import AutoSchema
from rest_framework.settings import api_settings
from rest_framework.utils import formatting
from django.utils.encoding import force_text, smart_text


logger = logging.getLogger(__name__)

PATH_PARAMETER_RE = re.compile(r'{(?P<parameter>\w+)}')
header_regex = re.compile('^[a-zA-Z][0-9A-Za-z_]*:')


class EndpointEnumerator(_EndpointEnumerator):
    def __init__(self, patterns=None, urlconf=None, request=None):
        super(EndpointEnumerator, self).__init__(patterns, urlconf)
        self.request = request

    def get_path_from_regex(self, path_regex):
        if path_regex.endswith(')'):
            logger.warning("url pattern does not end in $ ('%s') - unexpected things might happen", path_regex)
        return self.unescape_path(super(EndpointEnumerator, self).get_path_from_regex(path_regex))

    def should_include_endpoint(self, path, callback, app_name='', namespace='', url_name=None):
        if not super(EndpointEnumerator, self).should_include_endpoint(path, callback):
            #print('super not include')
            return False

        version = getattr(self.request, 'version', None)
        versioning_class = getattr(callback.cls, 'versioning_class', None)
        if versioning_class is not None and issubclass(versioning_class, versioning.NamespaceVersioning):
            if version and version not in namespace.split(':'):
                #print("version not include")
                return False

        if getattr(callback.cls, 'swagger_schema', object()) is None:
            #print("schema not include")
            return False

        return True

    def replace_version(self, path, callback):
        """If ``request.version`` is not ``None`` and `callback` uses ``URLPathVersioning``, this function replaces
        the ``version`` parameter in `path` with the actual version.
        :param str path: the templated path
        :param callback: the view callback
        :rtype: str
        """
        versioning_class = getattr(callback.cls, 'versioning_class', None)
        if versioning_class is not None and issubclass(versioning_class, versioning.URLPathVersioning):
            version = getattr(self.request, 'version', None)
            if version:
                version_param = getattr(versioning_class, 'version_param', 'version')
                version_param = '{%s}' % version_param
                if version_param not in path:
                    logger.info("view %s uses URLPathVersioning but URL %s has no param %s"
                                % (callback.cls, path, version_param))
                path = path.replace(version_param, version)

        return path

    def get_api_endpoints(self, patterns=None, prefix='', app_name=None, namespace=None, ignored_endpoints=None,final_arrays=None):
        """
        Return a list of all available API endpoints by inspecting the URL conf.
        Copied entirely from super.
        """
        if patterns is None:
            patterns = self.patterns
        #print(prefix)
        api_endpoints = []
        if ignored_endpoints is None:
            ignored_endpoints = set()

        for pattern in patterns:
            path_regex = prefix + get_original_route(pattern)
            #print(path_regex)
            if isinstance(pattern, URLPattern):
                try:
                    path = self.get_path_from_regex(path_regex)
                    callback = pattern.callback
                    url_name = pattern.name
                    if self.should_include_endpoint(path, callback, app_name or '', namespace or '', url_name):
                        path = self.replace_version(path, callback)

                        # avoid adding endpoints that have already been seen,
                        # as Django resolves urls in top-down order
                        if path in ignored_endpoints:
                            continue
                        ignored_endpoints.add(path)

                        for method in self.get_allowed_methods(callback):
                            endpoint = (path, method, callback)
                            api_endpoints.append(endpoint)
                except Exception:  # pragma: no cover
                    logger.warning('failed to enumerate view', exc_info=True)

            elif isinstance(pattern, URLResolver):
                nested_endpoints = self.get_api_endpoints(
                    patterns=pattern.url_patterns,
                    prefix=path_regex,
                    app_name="%s:%s" % (app_name, pattern.app_name) if app_name else pattern.app_name,
                    namespace="%s:%s" % (namespace, pattern.namespace) if namespace else pattern.namespace,
                    ignored_endpoints=ignored_endpoints,
                    final_arrays=final_arrays
                )
                #api_endpoints.extend(nested_endpoints)
            else:
                logger.warning("unknown pattern type {}".format(type(pattern)))

        #print(api_endpoints)
        api_endpoints = sorted(api_endpoints, key=endpoint_ordering)
        final_arrays.append({
            "prefix": prefix,
            "points": api_endpoints
        })
        return api_endpoints

    def unescape(self, s):
        """Unescape all backslash escapes from `s`.
        :param str s: string with backslash escapes
        :rtype: str
        """
        # unlike .replace('\\', ''), this corectly transforms a double backslash into a single backslash
        return re.sub(r'\\(.)', r'\1', s)

    def unescape_path(self, path):
        """Remove backslashe escapes from all path components outside {parameters}. This is needed because
        ``simplify_regex`` does not handle this correctly.
        **NOTE:** this might destructively affect some url regex patterns that contain metacharacters (e.g. \\w, \\d)
        outside path parameter groups; if you are in this category, God help you
        :param str path: path possibly containing
        :return: the unescaped path
        :rtype: str
        """
        clean_path = ''
        while path:
            match = PATH_PARAMETER_RE.search(path)
            if not match:
                clean_path += self.unescape(path)
                break
            clean_path += self.unescape(path[:match.start()])
            clean_path += match.group()
            path = path[match.end():]

        return clean_path


class OpenAPISchemaGenerator(object):
    endpoint_enumerator_class = EndpointEnumerator

    def __init__(self, name='API', version=''):
        self._gen = SchemaGenerator(name, None, '', None, None)
        self.version = version
        self.consumes = []
        self.produces = []

    @property
    def url(self):
        return self._gen.url

    def create_view(self, callback, method, request=None):
        """Create a view instance from a view callback as registered in urlpatterns.
        :param callback: view callback registered in urlpatterns
        :param str method: HTTP method
        :param request: request to bind to the view
        :type request: rest_framework.request.Request or None
        :return: the view instance
        """
        view = self._gen.create_view(callback, method, request)
        overrides = getattr(callback, '_swagger_auto_schema', None)
        if overrides is not None:
            # decorated function based view must have its decorator information passed on to the re-instantiated view
            for method, _ in overrides.items():
                view_method = getattr(view, method, None)
                if view_method is not None:  # pragma: no cover
                    setattr(view_method.__func__, '_swagger_auto_schema', overrides)

        setattr(view, 'swagger_fake_view', True)
        return view

    def get_schema(self, request=None, public=False):
        endpoints = self.get_endpoints(request)
        # return self.get_paths(endpoints, None, request, public=False)
        # import pdb; pdb.set_trace()
        register_api = self.get_register_api(endpoints, None, request, public=False)
        return self.handle_api_path(register_api)

    def get_endpoints(self, request):
        enumerator = self.endpoint_enumerator_class(self._gen.patterns, self._gen.urlconf, request=request)
        endpoints = []
        # import pdb; pdb.set_trace()
        enumerator.get_api_endpoints(final_arrays=endpoints)
        ret=[]
        for group in endpoints:
            #print(group)
            group_points=group['points']
            view_paths = defaultdict(list)
            view_cls = {}
            for path, method, callback in group_points:
                view = self.create_view(callback, method, request)
                # path = self.coerce_path(path, view)
                view_paths[path].append((method, view))
                view_cls[path] = callback.cls
            #返回的是一个json-dict
            ret.append({"prefix":group['prefix'],"points":{path: (view_cls[path], methods) for path, methods in view_paths.items()}})
        return ret

    def determine_path_prefix(self, paths):
        """
        Given a list of all paths, return the common prefix which should be
        discounted when generating a schema structure.
        This will be the longest common string that does not include that last
        component of the URL, or the last component before a path parameter.
        For example: ::
            /api/v1/users/
            /api/v1/users/{pk}/
        The path prefix is ``/api/v1/``.
        :param list[str] paths: list of paths
        :rtype: str
        """
        return self._gen.determine_path_prefix(paths)

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

        # TODO: SCHEMA_COERCE_METHOD_NAMES appears here and in `SchemaGenerator.get_keys`
        coerce_method_names = api_settings.SCHEMA_COERCE_METHOD_NAMES
        if header in sections:
            return sections[header].strip()
        if header in coerce_method_names:
            if coerce_method_names[header] in sections:
                return sections[coerce_method_names[header]].strip()
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

        return summary, description

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
            prefix = self.determine_path_prefix(list(endpoints.keys())) or ''

            assert '{' not in prefix, "base path cannot be templated in swagger 2.0"

            paths = {}
            for path, (view_cls, methods) in sorted(endpoints.items()):
                _path={}
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

            # #检查是否有basePath可以融合在一起
            # _current_len=len(ret)
            # for i in range(_current_len):
            #     _current_prefix=ret[i]['basePath']
            #     if prefix.find(_current_prefix)>=0:
            #         ret[i]['paths'].update(paths)
            #
            #         paths=None
            #         break
            #     elif _current_prefix.find(prefix)>=0:
            #         ret[i]['basePath']=prefix
            #         ret[i]['paths'].update(paths)
            #         paths=None
            #         break
            if not paths is None:
                ret.append({"basePath":prefix,"basePathArray":prefix.strip("/").split("/"),"paths":paths})

        return ret