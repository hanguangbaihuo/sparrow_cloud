import unittest
from unittest import mock

# from sparrow_cloud.cache.cache_manager import CacheManager


class MockModel(object):
    _meta = 'meta'


class MockModelsManager(object):
    model = MockModel()


class TestCacheManager(unittest.TestCase):
    """测试cachemanager"""

    def setUp(self):
        pass

    @mock.patch('django.db.models.Manager', side_effect=MockModelsManager())
    def test_cache_manager(self, Manager):
        from sparrow_cloud.cache.cache_manager import CacheManager
        # import pdb;pdb.set_trace()
        cache_manager = CacheManager()
        data = cache_manager.get(id='123')
        self.assertEqual(data, data)






