## sparrow cloud 组件介绍 ##
### Django SDK
* Cache Service : sparrow_cloud v1.7.0 以及之后的版本不在提供支持
* RestClient : 封装了request包和服务发现，正确请求返回解析后json数据， 错误请求返回HTTPException
* RequestsClient : 封装了request包和服务发现， 返回原生的request结果
* Message_Client : 将任务发送到rabbitmq, server端未开源
* Rabbitmq_Consumer : rabbitmq消息消费端，server端未开源
* Table_API : 接收查询条件返回 django model 序列化后的数据
* Api Schema Register : django subcommand, 主动注册API 描述到文档服务， server端未开源
* service_log : Log日志， 服务端未开源(v3.0.1 以及之后的版本不在提供支持)
* ding_talk : 发送消息到钉钉群，服务端未开源
* access_control verify : 访问控制验证，服务端未开源
* get_user_token : 获取用户token
* get_app_token : 获取app token


### Django Middleware ###
* JWT Middleware : 解析 JWT Token 
* Request Method Middleware : 兼容不支持 put/delete 请求
* ExceptionMiddleware : 异常通知

### rest_framework 中间件 ###
* UserID Authentication: 验证 user


## sparrow cloud组件 ##
[Service Log](#service_log)

[Cache Service](#cache_manager)

[RestClient](#restclient)

[RequestsClient](#requestsclient)

[Message_Client](#message_client)

[Rabbitmq_Consumer](#rabbitmq_consumer)

[Table_API](#table_api)

[Api Schema Register](#api-schema-register)

[ding_talk](#ding_talk)

[access_control_verify](#access_control_verify)

[access_control_register](#access_control_register)

[get_user_token](#get_user_token)

[get_app_token](#get_app_token)

## django中间件 ##
[JWT Middleware](#jwtmiddleware)

[Request Method Middleware](#method_middleware)

[ExceptionMiddleware](#exceptionmiddleware)

[TracingMiddleware](#tracingmiddleware)

## rest_framework中间件 ##
[UserID Authentication](#useridauthentication)


## installation ##

    pip install sparrowcloud

## 测试运行 ##

    运行所有测试:
        source tests/mock_configmap.sh && py.test tests && py.test access_control 
    运行单个测试:
        source tests/mock_configmap.sh && py.test tests/test_rest_client.py


## cache_manager

> 描述 ： cache_manager 会把model的get方法使用缓存

``` python
    # 依赖settings配置：
    import redis
    CACHE_REDIS_POOL = redis.ConnectionPool(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        decode_responses=True)


    # 使用方法：
    # 在models文件中导入
    from sparrow_cloud.sparrow_cloud.cache.cache_manager import CacheManager

    # 在需要使用缓存的model中加入
    objects = CacheManager()
    # demo中可查看示例
    # model 示例路径， sparrow_demo/models.py
```

## service_log

> 描述 ： 服务日志

``` python
    # 在 settings里面配置本服务配置
    SERVICE_CONF = {
        "NAME": "",  # 本服务的名称
    }

    # 使用：
    from sparrow_cloud.service_log.sender import send_log
     data = {
         "object_id": "test_object_id",
         "object_name": "test_object_name",
         "user_id": "888888889",
         "user_name": "tiger",
         "user_phone": "18700000401",
         "action": "跑路啦",
         "message": "enenenenenenenenene"
     }
    # result : True False
     result = send_log(data)


    # 参数说明(参数根据自己的业务场景传入即可):
    #     action: 服务自定义类型, string        （字段长度限制: 50）
    #     object_name: 对象名字, 可以是表名      （字段长度限制: 50）
    #     object_id: 对象ID, 业务逻辑自己传入    （字段长度限制: 20）
    #     user_id: 用户id, 操作用户             （字段长度限制: 64）
    #     user_name: 用户名称                  （字段长度限制: 50）
    #     user_phone: 用户手机号                （字段长度限制: 11）
    #     message: 消息   
```


## JWTMiddleware

> 描述：Token 解析
> 配置 JWTMiddleware 中间件需要的参数

``` python
    # 注册中间件
    MIDDLEWARE = (
        'sparrow_cloud.middleware.jwt_middleware.JWTMiddleware', # 放最上层

    # 将以下参数添加到settings.py
    JWT_MIDDLEWARE = {
        "JWT_SECRET": "", # JWT_SECRET, 必填
    }
```


## UserIDAuthentication
> 描述： user_id 解析
> 配置 UserIDAuthentication 认证需要的参数(仅兼容django2.2以上版本)

``` python
    SPARROW_AUTHENTICATION = {
        "USER_CLASS_PATH": "sparrow_cloud.auth.user.User",
    }
    # 参数说明： USER_CLASS_PATH： 路径中的User为中间件的User模版， 可以根据自己的需求重新创建User， 并将自己的 User路径按照模版格式放到：USER_CLASS_PATH下

    # 注册中间件
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'sparrow_cloud.auth.user_id_authentication.UserIDAuthentication',
        ),
    }
```

## METHOD_MIDDLEWARE
> 兼容阿里不支持 put/delete 请求
> 配置METHOD_MIDDLEWARE需要的参数

``` python
  # 注册 METHOD_MIDDLEWARE
  MIDDLEWARE_CLASSES = (
      'sparrow_cloud.middleware.methodconvert.MethodConvertMiddleware',  #兼容阿里请求方式中间件
  )
```

## TracingMiddleware
> 兼容阿里不支持 put/delete 请求
> 配置METHOD_MIDDLEWARE需要的参数

``` python
  MIDDLEWARE_CLASSES = (
      'sparrow_cloud.middleware.TracingMiddleware',  # 追踪链
  )
```

## restclient

> 服务调用中间件

``` python
    from sparrow_cloud.restclient import rest_client
    rest_client.post(SERVICE_CONF, api_path, timeout=10, json=api_list)

    # 参数说明:
    # SERVICE_CONF = "test-svc:8000"
    # timeout: 
    #     非必传，默认超时时间5秒
    #     传参方式：
    #         timeout=10       # 10秒为connect 和 read 的 timeout
    #         timeout=(5, 5)  # 分别定制：connect 和 read 的 timeout
    #         timeout=None    # Request 永远等待
    #     剩余参数与 requests.get/post 等方法保持一致
```    

## requestsclient

> 服务调用中间件（返回结果未封装）

``` python
    from sparrow_cloud.restclient import requests_client
    requests_client.post(SERVICE_CONF, api_path, timeout=10, json=api_list)

    # 参数说明:
    # SERVICE_CONF = "test-svc:8000"
    # timeout: 
    #     非必传，默认超时时间5秒
    #     传参方式：
    #         timeout=10       # 10秒为connect 和 read 的 timeout
    #         timeout=(5, 5)  # 分别定制：connect 和 read 的 timeout
    #         timeout=None    # Request 永远等待
    # ps:
    #   剩余参数与 requests.get/post 等方法保持一致      
```
      
## message_client

> 麻雀任务发送
> 1. 注册消息 2. 发送消息

``` python
    # 调用方式
    from sparrow_cloud.message_service.sender import send_task_v3
    # 非延时消息
    data = send_task_v3(message_code=message_code,
                        *args,
                        **kwargs)
    # 延时消息
    data = send_task_v3(message_code=message_code,
                    delay_time=200
                    *args,
                    **kwargs)
    # ps:
    #     message_code: 消息码
    #     delay_time: 延时时间，单位为秒

    =====================以下为旧版调用方式,不建议继续使用，会逐步弃用===========================    
    # 调用方式
    from sparrow_cloud.message_service.sender import send_task
    # 非延时消息
    data = send_task(exchange=exchange, 
                        routing_key=routing_key, 
                        message_code=message_code, 
                        retry_times=3,
                        *args,
                        **kwargs)
    # 延时消息
    data = send_task(exchange=exchange, 
                    routing_key=routing_key, 
                    message_code=message_code, 
                    retry_times=3,
                    delay=True,
                    delay_time=200
                    *args,
                    **kwargs)
    # ps:
    #     exchange: 交换机
    #     routing_key: 路由
    #     message_code: 消息码
    #     retry_times: 重试次数，非必填，默认重试次数为3次（每次间隔1秒）
    #     delay: 是否发送延时消息，默认为False，表示立即发送。如果设为True，则根据delay_time来设定延时时间
    #     delay_time: 延时时间，单位为秒
```


## rabbitmq_consumer

> 麻雀任务消费
> 1. 获取队列 2. 消费任务
``` python
    QUEUE_CONF_1 = {
        "QUEUE": "",
        "TARGET_FUNC_MAP": {
            "ORDER_PAY_SUC_ONLINE": "path",
        },
    }

    # ps:
    #     QUEUE_CONF_1  # 队列的配置
    #         QUEUE  # 队列名称
    #         TARGET_FUNC_MAP  # 队列消费的任务（字典中的键为message code，对应的值为执行该消息的任务函数路径字符串）


    # 调用方式：
    # 注册服务到 settings 下的 INSTALLED_APPS中
        
    INSTALLED_APPS = [
        "sparrow_cloud.apps.message_service",
    ]
        
    # 调用命令：
    python3 manage.py rabbitmq_consumer --queue QUEUE_CONF_1
        
    # ps：
    # 参数说明
    #     --queue ： 指定发送队列配置名称， 参照settings中QUEUE_CONF_1配置         
```


## table_api
> 接受查询条件返回django model 序列化后的数据
> 分为server端和client端

``` python

 # server 端配置
    # settings注册服务
    INSTALLED_APPS = [
        "sparrow_cloud.apps.table_api",
    ]
    # url配置
    urlpatterns = [
        path('table/api/', include("sparrow_cloud.apps.table_api.urls")),
    ]

 # client端调用 
    from sparrow_cloud.restclient import rest_client
    SERVICE_CONF = "sparrow-demo:8000"
    payload = {
        "app_lable_model":"app_lable.model",
        "filter_condition":{"product_id":"74101"}
    }
    response = rest_client.get(SERVICE_CONF, api_path='/table/api/', json=payload)
    #  返回的数据结构：{'code': 0, 'message': 'ok', 'data': [{}]}
    
    
    # ps:
    #     app_lable_model: app_name.model(app_name:INSTALLED_APPS里面注册的服务的名字, model:app_lable下的model名字，不区分大小写)
    #     filter_condition: 过滤数据， kwargs
    #     server端使用orm filter查询数据，当前版本不支持order_by
```

## API SCHEMA REGISTER
>描述：主动注册API 描述到文档服务 配置schema_command 需要的参数
``` python
    # settings 配置:
        # 注册服务到 settings 下的 INSTALLED_APPS中
        INSTALLED_APPS = [
            "sparrow_cloud.apps.schema_command",
        ]
    
        # 本服务配置
        SERVICE_CONF = {
            "NAME": "",  # 本服务的名称
            "SECRET": ""
        }
        
    
    # 调用方式:
        python3 manage.py register_api_schema
    # 使用说明:
    #     1、view支持@api_view注解方式，view_class支持GenericApiView，GenericViewSet及其子类
    #     2、接口描述书写在view函数或者view_class的__doc__上，建议使用markdown格式，展示更美观
  
```
>接口描述代码示例
```python
from rest_framework.decorators import api_view
from rest_framework.generics import  RetrieveUpdateDestroyAPIView
from rest_framework import  generics
from rest_framework.viewsets import ModelViewSet


@api_view(('GET',))
def get_user(request):
    """
    ### 获取用户信息 ####

        请求参数 id, 用户id
        返回
            {
                "user_id":"1",  # 用户ID
                "user_name":"Tom" # 用户名称
            }
    """


class UserApiView(RetrieveUpdateDestroyAPIView, generics.GenericAPIView):
    """
    get:
        ### 查询用户信息 ###

        请求参数 id, 用户id
        返回
            {
                "id":"1",  # 用户ID
                "user_name":"Tom" # 用户名称
            }
    delete:
        ### 删除用户 ###

        路径参数
            id 用户id
        返回
            404 用户id不存在
            204 删除成功
    """

    def put(self, request, *args, **kwargs):
        """
        ### 覆盖修改用户 ###

            请求参数
                {
                 "id":"1",  # 用户ID
                "user_name":"Tom" # 用户名称
                }
            返回 200 修改成功
        """
        return super(UserApiView, self).put(self, request, *args, **kwargs)


class CarViewSet(ModelViewSet):
    """
    list: 分页查询车辆
    retrieve:获取车辆信息
    update: 覆盖修改车辆
    partial_update: 部分修改车辆
    create: 创建车辆
    destroy: 删除车辆
    """
```

## DING_TALK
> ding_talk client SDK (将消息发送到钉钉群或微信群)
```python
    # 使用:
    from sparrow_cloud.dingtalk.sender import send_message
    from sparrow_cloud.authorization.token import get_app_token
    app_token = get_app_token()
    send_message(msg="test", code_list=["test", "test1"], channel="dingtalk", message_type="text", token=app_token)
    # 成功返回： {'code': 0, 'message': 'success'}
    # 错误返回： HTTPException

    # 参数说明：
    # msg:消息内容
    # code_list: 消息群code
    # channel: 消息发送的渠道("wechat", "dingtalk"), 默认 dingtalk
    # message_type:微信支持("text", "markdown")消息类型, 默认 text, 钉钉只支持text类型

```

## ExceptionMiddleware
> 中间件 (捕获程序异常，并发送消息到企业微信)
``` python
    # settings 配置
    MIDDLEWARE = [                 
        "sparrow_cloud.middleware.exception.ExceptionMiddleware"  
    ]

```

## ACCESS_CONTROL_VERIFY
> access_control_verify decorators (访问控制验证)
``` python
    # settings 配置
    SERVICE_CONF = {
        "NAME": "",  # value为本服务的注册名称
        "SECRET": "",
    }
    # 访问控制client端settings配置
    # SC_SKIP_ACCESS_CONTROL:  是否跳过访问控制，  True：跳过， false：不跳过

    
    # 使用方式
    # 函数视图使用方式示例
    from sparrow_cloud.access_control.decorators import access_control_fbv

    @api_view(('POST', 'GET', 'PUT', 'DELETE'))
    @access_control_fbv("permission_example1")  # 位置放到最下层
    def test(request, *args, **kwargs):
        return Response({"message": "ok"}, status=status.HTTP_200_OK)

    # 类视图使用方式(全部方法都验证)
    from sparrow_cloud.access_control.decorators import access_control_cbv_all

    @access_control_cbv_all("permission_example1")
    class ProductOperationList(generics.ListCreateAPIView):
        """请求方法：GET/POST"""
        pass
        
    # 类视图使用方式(根据method验证)
    from sparrow_cloud.access_control.decorators import access_control_cbv_method

    RESOURCE = {
    "post": "permission_example1", 
    "get": "permission_example2"
    }

    @access_control_cbv_method(RESOURCE)
    class ProductOperationList(generics.ListCreateAPIView):
        """请求方法：GET/POST"""
        pass
        
```

## get_user_token
> get_user_token (获取用户token)

```python
    # 获取用户token
    from sparrow_cloud.authorization.token import get_user_token
    user_token = get_user_token(user_id="21424kvjbcdjslafds")

```

## get_app_token
> get_app_token (获取用户token)

```python
    # 获取app token
    from sparrow_cloud.authorization.token import get_app_token
    app_token = get_app_token()

```
## Stargazers over time

[![Stargazers over time](https://starchart.cc/hanguangbaihuo/sparrow_cloud.svg)](https://starchart.cc/hanguangbaihuo/sparrow_cloud)

