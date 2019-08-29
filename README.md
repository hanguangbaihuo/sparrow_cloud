## sparrow cloud ##

### 安装 sparrow cloud ###
```
pip install git+https://github.com/hanguangbaihuo/sparrow_cloud.git

```


#### service_registry
> 说明： consul服务发现

```
依赖配置

```

#### cache_manager
> 说明 ： cache_manager 会把model的get方法使用缓存
```
依赖settings配置：

import redis
CACHE_REDIS_POOL = redis.ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True)
    
 
使用方法：
# 在models文件中导入
from sparrow_cloud.sparrow_cloud.cache.cache_manager import CacheManager

# 在需要使用缓存的model中加入
objects = CacheManager()


demo中可查看示例
model 示例路径， sparrow_demo/models.py


```