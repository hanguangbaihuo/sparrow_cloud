## sparrow cloud ##

### service_registry
> 说明： consul服务发现

```
依赖配置

```

### cache_manager
> 说明 ： cache_manager 会把model的get方法使用缓存
```
依赖settings配置：

import redis
CACHE_REDIS_POOL = redis.ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True)

```