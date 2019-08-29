## sparrow cloud ##

### 安装 sparrow cloud ###
```
pip install git+https://github.com/hanguangbaihuo/sparrow_cloud.git

```


#### service_registry
> 说明： consul服务发现

```
依赖settings配置：

CACHES = {
    'default': {
        'BACKEND': '',
        'LOCATION': '',
    }
}


# consul_service 依赖配置
CONSUL_CLIENT_ADDR = {
    "host": "127.0.0.1",  # consul host
    "port": 8500  # consul port
}

使用方法：
from sparrow_cloud.registry.service_registry import consul_service
# host 为默认参数，非必填， 如果传了此项参数， 会直接返回参数， 不过不传，则从consul中找服务地址
service_conf = {
        "service_name": "",  # k8s上的服务名称
        "host": "127.0.0.1:8001",  # 服务的真实host， 应用场景，consul服务故障， 或dev/test环境
    }
service_addr = consul_service(service_conf)
# 输出"127.0.0.1:8001"
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