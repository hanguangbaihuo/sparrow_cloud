"""
utils.py        # Shared helper functions

See schemas.__init__.py for package overview.
"""
import warnings

from rest_framework.mixins import RetrieveModelMixin


def is_list_view(path, method, view):
    """
    Return True if the given path/method appears to represent a list view.
    """
    if hasattr(view, 'action'):
        # Viewsets have an explicitly defined action, which we can inspect.
        return view.action == 'list'

    if method.lower() != 'get':
        return False
    if isinstance(view, RetrieveModelMixin):
        return False
    path_components = path.strip('/').split('/')
    if path_components and '{' in path_components[-1]:
        return False
    return True


def deprecate(msg, level_modifier=0):
    warnings.warn(msg, MigrationNotice, stacklevel=3 + level_modifier)


class MigrationNotice(DeprecationWarning):
    url = 'https://django-filter.readthedocs.io/en/master/guide/migration.html'

    def __init__(self, message):
        super().__init__('%s See: %s' % (message, self.url))
