"""
   Pagination 和 Filter组件
   drf3.9.0兼容drf3.4.7补丁
"""
# 使APIView的schema属性不依赖drf版本
import warnings
from rest_framework.pagination import BasePagination, PageNumberPagination, LimitOffsetPagination, CursorPagination
from ..schemas.utils import deprecate
from ..schemas.compat import coreapi, coreschema


# 为drf分页组件添加get_schema_field
def patch_paginator(instance):
    def get_page_schema_fields(instance, view):
        fields = [
            coreapi.Field(
                name=instance.page_query_param,
                required=False,
                location='query',
                schema=coreschema.Integer(
                    title='Page',
                    description='A page number within the paginated result set.'
                )
            )
        ]
        if instance.page_size_query_param is not None:
            fields.append(
                coreapi.Field(
                    name=instance.page_size_query_param,
                    required=False,
                    location='query',
                    schema=coreschema.Integer(
                        title='Page size',
                        description='Number of results to return per page.'
                    )
                )
            )
        return fields

    def get_limit_schema_fields(instance, view):
        return [
            coreapi.Field(
                name=instance.limit_query_param,
                required=False,
                location='query',
                schema=coreschema.Integer(
                    title='Limit',
                    description='Number of results to return per page.'
                )
            ),
            coreapi.Field(
                name=instance.offset_query_param,
                required=False,
                location='query',
                schema=coreschema.Integer(
                    title='Offset',
                    description='The initial index from which to return the results.'
                )
            )
        ]

    def get_cursor_schema_fields(instance, view):
        fields = [
            coreapi.Field(
                name=instance.cursor_query_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title='Cursor',
                    description='The pagination cursor value.'
                )
            )
        ]
        if instance.page_size_query_param is not None:
            fields.append(
                coreapi.Field(
                    name=instance.page_size_query_param,
                    required=False,
                    location='query',
                    schema=coreschema.Integer(
                        title='Page size',
                        description='Number of results to return per page.'
                    )
                )
            )
        return fields

    def get_base_schema_fields(instance, view):
        return []

    if issubclass(instance.__class__, PageNumberPagination):
        setattr(PageNumberPagination, "get_schema_fields", get_page_schema_fields)
    elif issubclass(instance.__class__, LimitOffsetPagination):
        setattr(LimitOffsetPagination, "get_schema_fields", get_limit_schema_fields)
    elif issubclass(instance.__class__, CursorPagination):
        setattr(CursorPagination, "get_schema_fields", get_cursor_schema_fields)
    elif issubclass(instance.__class__, BasePagination):
        setattr(BasePagination, "get_schema_fields", get_base_schema_fields)


# 为drf filter组件添加get_schema_fields
def patch_filter_backend(instance):
    def get_backend_filter_schema_fields(view):
        """
            from django-filter-2.2.0 rest_framework.backends.get_schema_fields
        """
        try:
            queryset = view.get_queryset()
        except Exception:
            queryset = None
            warnings.warn(
                "{} is not compatible with schema generation".format(view.__class__)
            )
        filterset_class = instance.get_filterset_class(view, queryset)
        return [] if not filterset_class else [
            coreapi.Field(
                name=field_name,
                required=field.extra['required'],
                location='query',
                schema=instance.get_coreschema_field(field)
            ) for field_name, field in filterset_class.base_filters.items()
        ]

    def get_filterset_class(self, view, queryset=None):
        """
        Return the `FilterSet` class used to filter the queryset.
        """
        filterset_class = getattr(view, 'filterset_class', None)
        filterset_fields = getattr(view, 'filterset_fields', None)

        # TODO: remove assertion in 2.1
        if filterset_class is None and hasattr(view, 'filter_class'):
            deprecate(
                "`%s.filter_class` attribute should be renamed `filterset_class`."
                % view.__class__.__name__)
            filterset_class = getattr(view, 'filter_class', None)

        # TODO: remove assertion in 2.1
        if filterset_fields is None and hasattr(view, 'filter_fields'):
            deprecate(
                "`%s.filter_fields` attribute should be renamed `filterset_fields`."
                % view.__class__.__name__)
            filterset_fields = getattr(view, 'filter_fields', None)

        if filterset_class:
            filterset_model = filterset_class._meta.model

            # FilterSets do not need to specify a Meta class
            if filterset_model and queryset is not None:
                assert issubclass(queryset.model, filterset_model), \
                    'FilterSet model %s does not match queryset model %s' % \
                    (filterset_model, queryset.model)

            return filterset_class

        if filterset_fields and queryset is not None:
            MetaBase = getattr(self.filterset_base, 'Meta', object)

            class AutoFilterSet(self.filterset_base):
                class Meta(MetaBase):
                    model = queryset.model
                    fields = filterset_fields

            return AutoFilterSet

        return None

    def get_search_schema_fields(view):
        return [
            coreapi.Field(
                name=instance.search_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title='Search',
                    description='A search term.'
                )
            )
        ]

    def get_order_schema_fields(view):
         return [
            coreapi.Field(
                name=instance.ordering_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title='Ordering',
                    description='Which field to use when ordering the results.'
                )
            )
        ]
    if instance.__class__.__name__ == "DjangoFilterBackend":
        setattr(instance, "get_schema_fields", get_backend_filter_schema_fields)
        setattr(instance, "get_filterset_class", get_filterset_class)
    if instance.__class__.__name__ == "SearchFilter":
        setattr(instance, "get_schema_fields", get_search_schema_fields)
    if instance.__class__.__name__ == "OrderingFilter":
        setattr(instance, "get_schema_fields", get_order_schema_fields)



