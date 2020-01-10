from django.db import models
from django.conf import settings


class CacheManager(models.Manager):

    def get(self, *args, **kwargs):
        # if self.model and self.model._meta and self.model._meta.db_table:
        #     pk_name = self.model._meta.pk.attname
        #     if len(kwargs)==1 and (pk_name in kwargs or 'pk' in kwargs):
        #         table_name = self.model._meta.db_table
        #         field_objs = self.model._meta.fields
        #         field_names = [field.attname for field in field_objs]
        #         pk_value = kwargs[pk_name]
        #         redis_prefix = settings.REDIS_CACHE["REDIS_HASH_PRIFIX"]
        #         redis_hash_key = redis_prefix + ":"+table_name+":"+pk_value
        #         import redis
        #         r = redis.Redis(connection_pool=settings.CACHE_REDIS_POOL)
        #         redis_hash_value = r.hmget(redis_hash_key, field_names)
        #         if redis_hash_value is not None:
        #             redis_obj = self.none()
        #             exist_flag = False
        #             for k, v in zip(field_names, redis_hash_value):
        #                 if v is not None:
        #                     exist_flag = True
        #                     setattr(redis_obj, k, v)
        #             if exist_flag:
        #                 return redis_obj
        db_obj = super(CacheManager, self).get(*args, **kwargs)
        return db_obj
