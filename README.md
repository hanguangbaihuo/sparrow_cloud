## sparrow cloud ##

## 测试运行 ##

    运行所有测试: 
        py.test
    运行单个测试:
        py.test tests/test_rest_client.py


### 安装 sparrow cloud ###
```
pip install git+https://github.com/hanguangbaihuo/sparrow_cloud.git

```


#### service_registry
> 描述： consul服务发现

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
    "HOST": "127.0.0.1",  # consul host, 必填
    "PORT": 8500  # consul port, 必填
}

使用方法：
from sparrow_cloud.registry.service_registry import consul_service
# host 为默认参数，非必填， 如果传了此项参数， 会直接返回参数， 不过不传，则从consul中找服务地址
service_conf = {
        "NAME_SVC": "",  # k8s上的服务名称
        "HOST": "127.0.0.1:8001",  # 服务的真实host， 应用场景，consul服务故障， 或dev/test环境
    }
service_addr = consul_service(service_conf)
# 输出"127.0.0.1:8001"
```
#### cache_manager
> 描述 ： cache_manager 会把model的get方法使用缓存
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


* * *

#### JWTMiddleware
> 描述：Token 解析

#### 配置 JWTMiddleware 中间件需要的参数
> 将以下参数添加到settings.py
```
JWT_MIDDLEWARE = {
    "JWT_SECRET": "", # JWT_SECRET, 必填
}
``` 
>参数说明： JWT_SECRET : jwt_secret

#### 注册 JWTMiddleware

> 注册中间件
```
MIDDLEWARE = (
    'sparrow_cloud.middleware.jwt_middleware.JWTMiddleware', # 放最上层
```


* * *


#### UserIDAuthentication
> 描述： user_id 解析

#### 配置 UserIDAuthentication 认证需要的参数(仅兼容django2.2以上版本)

```
SPARROW_AUTHENTICATION = {
    "USER_CLASS_PATH": "sparrow_cloud.auth.user.User",
}

# 参数说明： USER_CLASS_PATH： 路径中的User为中间件的User模版， 可以根据自己的需求重新创建User， 并将自己的User路径按照模版格式放到：USER_CLASS_PATH下 

# 注册中间件

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'sparrow_cloud.auth.user_id_authentication.UserIDAuthentication',
    )
}
```

#### permission_command  API权限服务
> 描述： 主动注册API到权限服务
#### 配置 permission_command 需要的参数

```
# 本服务配置
SERVICE_CONFIG = {
    "NAME": "",  # 本服务的名称
}


# API 权限服务配置
PERMISSION_SERVICE_CONFIG = {
    "SERVICE_NAME": "SPARROW_PERMISSION",  # 权限服务的名称，默认为：SPARROW_PERMISSION
    "NAME_SVC": "",  #  权限服务，服务发现的名称
    "HOST": "",  # 默认为""
    "REGISTER_API": ""  # 权限服务的PATH
}

```


#### METHOD_MIDDLEWARE
> 兼容阿里不支持 put/delete 请求
#### 配置METHOD_MIDDLEWARE需要的参数
```
# 将以下参数添加到settings.py
METHOD_MIDDLEWARE = {
    "METHOD_MAP": ('PUT', 'DELETE',), 
}
# 注册 METHOD_MIDDLEWARE
MIDDLEWARE_CLASSES = (
    'sparrow_django_common.middleware.methodconvert.MethodConvertMiddleware',      #兼容阿里请求方式中间件
)

```