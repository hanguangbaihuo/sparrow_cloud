# -*- coding: utf-8 -*-
from django.conf import settings
from jaeger_client import Tracer, ConstSampler
from jaeger_client.reporter import NullReporter
from jaeger_client.codecs import B3Codec
from opentracing.ext import tags
from opentracing.propagation import Format
from sparrow_cloud.middleware.base.base_middleware import MiddlewareMixin
import logging
import opentracing
import six


logger = logging.getLogger(__name__)


class TracingMiddleware(MiddlewareMixin):
    '''
    __init__() is called only once, when the Web server starts.
    '''
    def __init__(self, get_response=None):
        '''
        Init a global tracer
        '''
        self.get_response = get_response
        self._init_tracer()

    def _init_tracer(self):
        service_name = ''
        try:
            value = getattr(settings, 'SERVICE_CONF', '')
            if value:
                service_name = value.get('NAME', '')
        except Exception as e:
            logger.error('SERVICE_CONF:NAME is not set in settings. {}'.format(str(e)))
        # create a global tracer first
        tracer = Tracer(
            one_span_per_rpc=True,
            service_name=service_name,
            reporter=NullReporter(),
            sampler=ConstSampler(decision=True),
            extra_codecs={Format.HTTP_HEADERS: B3Codec()}
        )
        opentracing.set_global_tracer(tracer)

    def process_view(self, request, view_func, view_args=None, view_kwargs=None):
        '''
        process_view() should return either None or an HttpResponse object.
        If it returns None, Django will continue processing this request,
        executing any other process_view() middleware and, then, the appropriate view. 
        '''
        # strip headers for trace info
        headers = {}
        for k, v in six.iteritems(request.META):
            k = k.lower().replace('_', '-')
            if k.startswith('http-'):
                k = k[5:]
            headers[k] = v
        # logger.debug('=================== headers :  {}'.format(headers))
        tracer = opentracing.global_tracer()
        # logger.debug('=================== tracer :  {}'.format(tracer))
        span_ctx = tracer.extract(
            Format.HTTP_HEADERS,
            headers
        )
        rpc_tag = {
            tags.COMPONENT: 'django',
            tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
            tags.HTTP_METHOD: request.method,
            tags.HTTP_URL: request.get_full_path(),
        }
        operation_name = view_func.__name__
        scope = tracer.start_active_span(
            operation_name=operation_name,
            child_of=span_ctx,
            tags=rpc_tag
        )
        span = scope.span
        # import pdb; pdb.set_trace()
        # logger.debug('=================== span id:  {}'.format(span.span_id))
        # logger.debug('=================== span trace id:  {}'.format(span.trace_id))
        # logger.debug('=================== span parent id:  {}'.format(span.parent_id))
        # logger.debug('=================== span tags:  {}'.format(span.tags))
        
    
    # def process_request(self, request, response):
    #     return response

    # def process_exception(self, request, exception):
    #     self._tracing._finish_tracing(request, error=exception)

    # def process_response(self, request, response):
    #     self._tracing._finish_tracing(request, response=response)
    #     return response
