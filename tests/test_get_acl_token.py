import os
import time
import unittest
from django.conf import settings
from sparrow_cloud.utils.get_hash_key import get_hash_key
from sparrow_cloud.utils.get_acl_token import get_acl_token


class TestGetACLToken(unittest.TestCase):

    def setUp(self):
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"

    def test_get_acl_token_from_settings(self):
        acl_token_key = get_hash_key("ACL_TOKEN")
        setattr(settings, acl_token_key, {'acl_token': 'ACL_TOKEN88888888888', 'time': time.time()})
        self.assertEqual(get_acl_token('acl_test'), 'ACL_TOKEN88888888888')

    def test_get_acl_token_from_cache(self):
        from django.core.cache import cache
        acl_token_key = get_hash_key("ACL_TOKEN")
        cache.set(acl_token_key, {'acl_token': 'ACL_TOKEN1010101010', 'time': time.time()})
        self.assertEqual(get_acl_token('acl_test'), 'ACL_TOKEN1010101010')


