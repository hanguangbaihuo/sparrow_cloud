import io
import pytest
import unittest
from django.core.management import call_command
from django.test.utils import override_settings
from sparrow_cloud.apps.permission_command.management.commands import register_api_permission


class TestRegisterApiPermission(unittest.TestCase):
    """Tests for register_api_permission command"""

    def setUp(self):
        self.out = io.StringIO()

    @override_settings(ROOT_URLCONF=__name__)
    def test_add_arguments(self):
        import pdb;pdb.set_trace()
        call_command(register_api_permission,
                     '-d',
                     stdout=self.out)
        # parser.add_argument('--format', dest="format", choices=['openapi', 'openapi-json', 'corejson'],
        #                     default='openapi', type=str)
        # parser.add_argument('--title', dest="title", default='', type=str)
        # parser.add_argument('--url', dest="url", default=None, type=str)
        # parser.add_argument('--description', dest="description", default=None, type=str)
        # if self.get_mode() == COREAPI_MODE:
        #     parser.add_argument('--format', dest="format", choices=['openapi', 'openapi-json', 'corejson'],
        #                         default='openapi', type=str)
        # else:
        #     parser.add_argument('--format', dest="format", choices=['openapi', 'openapi-json'], default='openapi',
        #                         type=str)
        # parser.add_argument('--urlconf', dest="urlconf", default=None, type=str)
        # parser.add_argument('--generator_class', dest="generator_class", default=None, type=str)

        # parser.add_argument(
        #     '-d', '--django', dest='dj_ver',
        #     default="2", choices=["1", "2"],
        #     help='指定django的版本，可选值为1或2。如果django版本>=1.11,请选择2'
        # )
