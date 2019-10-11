"""
The `compat` module provides support for backwards compatibility with older
versions of Django/Python, and compatibility wrappers around optional packages.
"""
import coreapi
import coreschema
try:
    from django.urls import (
        URLPattern,
        URLResolver,
    )
except ImportError:
    try:
        from django.urls import (
            RegexURLPattern as URLPattern,
            RegexURLResolver as URLResolver,
        )
    except ImportError:
        from django.core.urlresolvers import (
            RegexURLPattern as URLPattern,
            RegexURLResolver as URLResolver,
        )


try:
    from django.core.validators import ProhibitNullCharactersValidator
except ImportError:
    ProhibitNullCharactersValidator = None


def get_original_route(urlpattern):
    """
    Get the original route/regex that was typed in by the user into the path(), re_path() or url() directive. This
    is in contrast with get_regex_pattern below, which for RoutePattern returns the raw regex generated from the path().
    """
    if hasattr(urlpattern, 'pattern'):
        # Django 2.0
        return str(urlpattern.pattern)
    else:
        # Django < 2.0
        return urlpattern.regex.pattern


# uritemplate is required for OpenAPI and CoreAPI schema generation
try:
    import uritemplate
except ImportError:
    uritemplate = None
