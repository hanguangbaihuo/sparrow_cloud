## sparrow cloud组件 ##

[Service Discovery](#service_registry)

[Cache Service](#cache_manager)

[API Permission Register](#api-permission-register)

[RestClient](#restcliet-使用说明)

[Message_Client](#message_client)

[Rabbitmq_Consumer](#rabbitmq_consumer)

[Table_API](#table_api)


## django中间件 ##
[JWT Middleware](#jwtmiddleware)

[Request Method Middleware](#method_middleware)

[Permission Verify Middleware](#permission_middleware)


## rest_framework中间件 ##
[UserID Authentication](#useridauthentication)




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
from sparrow_cloud.registry.service_discovery import consul_service
> consul_service(SERVICE_CONF)
> "127.0.0.1:8001"

参数说明:
  SERVICE_CONF = {
        "ENV_NAME": "PERMISSION_REGISTER_NAME_HOST",
        "VALUE": "sprrow-permission-svc"
    },
    ENV_NAME: 用来覆盖 consul 的环境变量名
    VALUE: consul服务注册名字
如果有环境变量 PERMISSION_REGISTER_NAME_HOST 存在, 则覆盖 consul

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
    ),
}
```

## API Permission Register

> 描述： 主动注册API到权限服务
> 配置 permission_command 需要的参数

```
    settings 配置:
        # 注册服务到 settings 下的 INSTALLED_APPS中
        INSTALLED_APPS = [
            "sparrow_cloud.apps.permission_command",
        ]
    
        # 本服务配置
        SERVICE_CONF = {
            "NAME": "",  # 本服务的名称
        }
        
        # 注册服务的配置
        SPARROW_PERMISSION_REGISTER_CONF = {
            "PERMISSION_SERVICE": {
                "ENV_NAME": "PERMISSION_SERVICE_HOST",
                "VALUE": "xxxxx-svc",
            },
            "API_PATH": "/api/permission_i/register/",
        }

    调用方式：
        python3 manage.py register_api_permission  -d 2

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
      'sparrow_cloud.middleware.methodconvert.MethodConvertMiddleware',  #兼容阿里请求方式中间件
  )
```

## PERMISSION_MIDDLEWARE
> 权限中间件
> 配置PERMISSION_MIDDLEWARE需要的参数

```
# 将以下参数添加到settings.py
PERMISSION_MIDDLEWARE = {
    "PERMISSION_SERVICE": {
        # ENV_NAME 为覆盖consul的默认值, 环境变量名称示例：服务名称_HOST， 只需要给一个环境变量的NAME，不需要给VALUE
        "ENV_NAME": "",
        # VALUE 为服务发现的注册名称
        "VALUE": "",
    },
    "API_PATH": "",
    "FILTER_PATH": [''],  # 使用权限验证中间件， 如有不需要验证的URL， 可添加到列表中
    # 是否启用权限中间件， SKIP_PERMISSION:True, 则跳过中间件，如果不配置SKIP_PERMISSION，或者SKIP_PERMISSION:False，则不跳过中间件
    "SKIP_PERMISSION": False
}

注册中间件
MIDDLEWARE = [
    'sparrow_cloud.middleware.api_permission.PermissionMiddleware',
]

PS: 如果未配置 CONSUL_CLIENT_ADDR, 需要配置该参数, 权限中间件依赖 consul
```

## restclient 使用说明

> 服务调用中间件

```
  from sparrow_cloud.restclient import rest_client
  rest_client.post(SERVICE_CONF, api_path, json=api_list)
```
    参数说明:
    SERVICE_CONF = {
        "ENV_NAME": "PERMISSION_REGISTER_NAME_HOST",
        "VALUE": "sprrow-permission-svc",
    },
    ENV_NAME: 用来覆盖 consul 的环境变量名
    VALUE: consul服务注册名字
    ps:
      剩余参数与 requests.get/post 等方法保持一致
      

## requestsclient 使用说明

> 服务调用中间件（返回结果未封装）

```
  from sparrow_cloud.restclient import requests_client
  requests_client.post(SERVICE_CONF, api_path, json=api_list)
```
    参数说明:
    SERVICE_CONF = {
        "ENV_NAME": "PERMISSION_REGISTER_NAME_HOST",
        "VALUE": "sprrow-permission-svc",
    },
    ENV_NAME: 用来覆盖 consul 的环境变量名
    VALUE: consul服务注册名字
    ps:
      剩余参数与 requests.get/post 等方法保持一致      

      
## message_client 使用说明

> 麻雀任务发送
> 1. 注册消息 2. 发送消息

```
    settings配置
        MESSAGE_SENDER_CONF = {
            "SERVICE_CONF": {
                "ENV_NAME": "MESSAGE_REGISTER_NAME_HOST",
                "VALUE": "sparrow-task-test-svc",
            },
            "API_PATH": "/api/sparrow_task/producer/send/",
        }
        ps: 
            MESSAGE_SENDER_CONF  # 配置
                SERVICE_CONF  # message_client依赖consul
                API_PATH  # message_client 发送消息地址
    
    调用方式：
        from sparrow_cloud.message_service.sender import send_task
        data = send_task(exchange=exchange, 
                         routing_key=routing_key, 
                         message_code=message_code, 
                         *args,
                         **kwargs)
        ps:
           exchange: 交换机
           routing_key: 路由
           message_code: 消息码
```


## rabbitmq_consumer 使用说明

> 麻雀任务消费
> 1. 获取队列 2. 消费任务
```
    settings配置

        SPARROW_RABBITMQ_CONSUMER_CONF = {

            "MESSAGE_BROKER_CONF": {
                "USER_NAME": "test",
                "PASSWORD": "jfdskafsake",
                "VIRTUAL_HOST": "sparrow_test",
                "BROKER_SERVICE_CONF": {
                    "ENV_NAME": "SPARROW_BROKER_HOST",
                    "VALUE": "sparrow-demo",
                },
            },
            "MESSAGE_BACKEND_CONF": {
                "BACKEND_SERVICE_CONF": {
                        "ENV_NAME": "SPARROW_BACKEND_HOST",
                        "VALUE": "sparrow-demo",
                },
                "API_PATH": "/api/sparrow_task/task/update/",
            }
        }

        QUEUE_CONF_1 = {
            "QUEUE": "ORDER_PAY_SUC_ALL",
            "TARGET_FUNC_MAP": {
                "ORDER_PAY_SUC_ONLINE": "message_service.task.task1",
            },
        }


        ps:
                SPARROW_RABBITMQ_CONSUMER_CONF  # consumer的配置
                    MESSAGE_BROKER_CONF  # rabbitmq配置
                        USER_NAME # 用户名
                        PASSWORD # 密码
                        VIRTUAL_HOST # 虚拟主机
                        BROKER_SERVICE_CONF  # 依赖consul服务的配置
                    MESSAGE_BACKEND_CONF
                        BACKEND_SERVICE_CONF # 依赖consul服务的配置
                        API_PATH # api 路径
                QUEUE_CONF_1  # 队列的配置
                    QUEUE  # 队列名称
                    TARGET_FUNC_MAP  # 队列消费的任务（字典中的键为message code，对应的值为执行该消息的任务函数路径字符串）


    调用方式：
        注册服务到 settings 下的 INSTALLED_APPS中
        
        INSTALLED_APPS = [
            "sparrow_cloud.apps.message_service",
        ]
        
        调用命令：
        python3 manage.py rabbitmq_consumer --queue QUEUE_CONF_1
        
        ps：
        参数说明
            --queue ： 指定发送队列配置名称， 参照settings中QUEUE_CONF_1配置
            
    
```


## table_api 使用说明
> 接受查询条件返回django model 序列化后的数据
> 分为server端和client端

```

 # server 端配置
    # settings注册服务
    INSTALLED_APPS = [
        "sparrow_cloud.apps.table_api",
    ]
    url配置
    urlpatterns = [
    path('table/api/', include("sparrow_cloud.apps.table_api.urls")),
    ]


 # client端调用 
    from sparrow_cloud.restclient import rest_client
    SERVICE_CONF = {
             "ENV_NAME": "PERMISSION_REGISTER_NAME_HOST",
             "VALUE": "sprrow-permission-svc"
         }
    payload = {
        "app_lable":"product",
        "model":"SparrowProductsProductoperationlog",
        "filter_condition":{"product_id":"74101"}
    }
    response = rest_client.get(SERVICE_CONF, api_path='/api/table_api/', json=payload)
    #  返回的数据结构：{'code': 0, 'message': 'ok', 'data': [{}]}
    
    
    ps:
        app_lable: app_name(INSTALLED_APPS里面注册的服务的名字)
        model: app_lable下的model名字，不区分大小写
        filter_condition: 过滤数据， kwargs
        server端使用orm filter查询数据，当前版本不支持order_by
```