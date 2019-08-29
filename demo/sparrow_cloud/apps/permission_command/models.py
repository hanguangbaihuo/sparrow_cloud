# from django.db import models
# from django.utils import timezone
# import uuid
# from sparrow_cloud.cache.cache_manager import CacheManager

# class CacheTest(models.Model):
#     id = models.CharField(max_length=100,primary_key=True,default=uuid.uuid4().hex)
#     name = models.CharField(max_length=35, blank=True)
#     created_time = models.DateTimeField(auto_now_add=True)
#     updated_time = models.DateTimeField(default=timezone.now)
#     objects = CacheManager()