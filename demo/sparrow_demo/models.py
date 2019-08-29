from django.db import models
from sparrow_cloud.cache.cache_manager import CacheManager


class Demo(models.Model):
    objects = CacheManager()
