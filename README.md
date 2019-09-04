## sparrow cloud组件 ##

[Service Discovery](#service_registry)

[Cache Service](#cache_manager)

[API Permission Register](#api-permission-register)

[RestClient](#restcliet-使用说明)


## sparrow cloud中间件 ##
[JWT Middleware](#jwtmiddleware)

[UserID Authentication](#useridauthentication)

[Request Method Middleware](#method_middleware)

[Permission Verify Middleware](#permission_middleware)

## installation ##

    pip install sparrowcloud

## 测试运行 ##

    运行所有测试:
        py.test
    运行单个测试:
        py.test tests/test_rest_client.py

## service_registry

> 描述： consul服务发现
> sparrow_cloud 项目的许多组件对 consul服务发现 有重度依赖, 需配置 consul

```
# 在 settings里面配置 consul参数
CONSUL_CLIENT_ADDR = {
    "HOST": os.environ.get("CONSUL_IP", "127.0.0.1"),  # 在k8s上的环境变量类型：变量/变量引用
    "PORT": os.environ.get("CONSUL_PORT", 8500)
}

使用方法：
from sparrow_cloud.registry.service_registry import consul_service
> consul_service("SERVICE_SETTINGS_KEY_NAME")
> "127.0.0.1:8001"

参数说明:
  SERVICE_SETTINGS_KEY_NAME: settings里面的 key 值
例如, 在 settings 里面有如下配置:
  SPARROW_PRODUCT_REGISTER_NAME = "sparrow-product-svc"
  则, 参数为 : "SPARROW_PRODUCT_REGISTER_NAME"
  consul_service("SPARROW_PRODUCT_REGISTER_NAME")
如果有环境变量 SPARROW_PRODUCT_REGISTER_NAME_HOST 存在, 则覆盖 consul

consul_service: 返回地址的方法:
  1 如果有 SERVICE_SETTINGS_KEY_NAME_HOST (参数名字_HOST)环境变量存在, 则直接返回该环境变量的值作为地址.
  2 如果没有, 则使用 consul 服务发现中心返回地址
```

## cache_manager

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

## JWTMiddleware

> 描述：Token 解析
> 配置 JWTMiddleware 中间件需要的参数

```
注册中间件
MIDDLEWARE = (
    'sparrow_cloud.middleware.jwt_middleware.JWTMiddleware', # 放最上层

将以下参数添加到settings.py
JWT_MIDDLEWARE = {
    "JWT_SECRET": "", # JWT_SECRET, 必填
}
```

## UserIDAuthentication
> 描述： user_id 解析
> 配置 UserIDAuthentication 认证需要的参数(仅兼容django2.2以上版本)

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

## API Permission Register

> 描述： 主动注册API到权限服务
> 配置 permission_command 需要的参数

```
# 本服务配置
SERVICE_CONF = {
    "NAME": "",  # 本服务的名称
}


# API 权限服务配置
### api permission 依赖 ###
环境变量名字
SPARROW_PERMISSION_REGISTER_NAME = "sparrow-purchase-limit-svc"
SPARROW_PERMISSION_REGISTER_API = "/api/permission_i/register/"

ps: 环境变量名字不能修改, SPARROW_PERMISSION_REGISTER_NAME 可由
SPARROW_PERMISSION_REGISTER_NAME_HOST = "127.0.0.1:8001" 覆盖

```
## METHOD_MIDDLEWARE
> 兼容阿里不支持 put/delete 请求
> 配置METHOD_MIDDLEWARE需要的参数

```
  # 将以下参数添加到settings.py #
  METHOD_MIDDLEWARE = {
      "METHOD_MAP": ('PUT', 'DELETE',),
  }
  # 注册 METHOD_MIDDLEWARE
  MIDDLEWARE_CLASSES = (
      'sparrow_django_common.middleware.methodconvert.MethodConvertMiddleware',      #兼容阿里请求方式中间件
  )
```

## PERMISSION_MIDDLEWARE
> 权限中间件
> 配置PERMISSION_MIDDLEWARE需要的参数
```
# 将以下参数添加到settings.py
PERMISSION_MIDDLEWARE = {
    # 权限验证服务的配置
    "PERMISSION_SERVICE":{
        "NAME": "", #服务名称（k8s上的服务名）, 必填
        "HOST": "", #IP, 开发环境必填（开发环境使用转发到本地的host）
        "PORT": 8001, # 服务端口, dev环境需要注意， 配置写的端口需要和转发到本地的端口保持一致, 必填
        "PATH": "", # url, 必填
    },
    "FILTER_PATH" : [''], # 使用权限验证中间件， 如有不需要验证的URL， 可添加到列表中
    "SKIP_PERMISSION": False, # 是否启用权限中间件， SKIP_PERMISSION:True, 则跳过中间件， 如果不配置SKIP_PERMISSION，或者SKIP_PERMISSION:False，则不跳过中间件
}

注册中间件
MIDDLEWARE = [
    'sparrow_cloud.middleware.api_permission.PermissionMiddleware',
]

PS: 如果未配置 CONSUL_CLIENT_ADDR, 需要配置该参数, 权限中间件依赖 consul
```

## restcliet 使用说明

> 服务调用中间件
```
  from sparrow_cloud.restclient import rest_client
  rest_client.post(service_settings_key, api_path, json=api_list)
```
    参数说明:
    service_settings_key:
      SERVICE_REGISTER_NAME = "xxxxx-svc"
      api_path: 请求的服务路径,例如 /api/xx/yy/
    ps:
      剩余参数与 requests.get/post 等方法保持一致