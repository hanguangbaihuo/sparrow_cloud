# Changelog
此项目的所有显着更改都将记录在此文件中。


格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [Unreleased]

## [3.1.2] - 2021-03-24
### Changed
- add timeout for all methods of rest_client

## [3.1.1] - 2021-02-23
### Added
- add message detail "task_info"  for rabbitmq consumer controller when calling update task_result api 

## [3.1.0] - 2021-1-28
### Added
- distributed_lock package to add or remove_lock

## [3.0.10] - 2021-1-14
### Changed
- support text/image/markdown/card_text/card_image type message to send in app_message

## [3.0.9] - 2021-1-8
### Changed
- raise raw exception when requests occur exception in requests_client

## [3.0.8] - 2021-1-8
### Changed
- add timeout for all methods of requests_client

## [3.0.7] - 2020-12-23
### Changed
- sdk: remove msg_data type check in send_message function of app_message
- remove support for python 3.5 due to update cryptography from 2.8 to 3.3.1
- JWT_SECRET environment variable have priority over setting in decode_jwt function

## [3.0.6] - 2020-11-18
### Added
- sdk: app_message
## [3.0.5] - 2020-11-10
### Changed
- consumer: fix bug
  
## [3.0.4] - 2020-10-30
### Changed
- methodconvert: fix bug
  
## [3.0.3] - 2020-10-30
### Changed
- methodconvert: fix bug
  
## [3.0.2] - 2020-10-30
### Changed
- sparrow_rabbitmq_consumer: fix bug

## [3.0.1] - 2020-10-30
### Changed
- sparrowcloud/service_log move the setting value to configmap

## [3.0.0] - 2020-10-29
### Changed
- sparrowcloud move the setting value to configmap
  
## [2.0.11] - 2020-10-16
### Added
- send_task_v3

## [2.0.10] - 2020-10-12
### Changed
- message_service import decimal & collections

## [2.0.9] - 2020-9-29
### Added
- send_task_v2
  
### Changed
- consumer Record on failure
  
## [2.0.8] - 2020-7-31
### Changed
- access_control fix bug

## [2.0.7] - 2020-7-7
### Changed
- SDK:get_user_token 
- SDK:get_app_token

## [2.0.6] - 2020-7-7
### Changed
- change dingtalk

## [2.0.4] - 2020-7-7
### Changed
- SDK:get_user_token 
- SDK:get_app_token

## [2.0.3] - 2020-7-7
### Changed
- SDK:get_user_token 
- SDK:get_app_token

## [2.0.3] - 2020-7-7
### Added
- SDK:get_user_token 
- SDK:get_app_token

## [2.0.0] - 2020-6-29
### Changed
- Middleware configuration
- rest client configuration
- requests client configuration
- message_client configuration
- rabbitmq_consumer configuration
- table_api configuration
- API SCHEMA REGISTER configuration
- service_log configuration
- DING_TALK configuration
- ACCESS_CONTROL_VERIFY configuration

### Remove
- service_configuration
- ACL Middleware
- API Permission Register


## [1.9.7] - 2020-6-18
### Changed
- change cbv Undecorated method does not go through user verification

## [1.9.6] - 2020-6-17
### Changed
- change fbv/cbv response.content

## [1.9.5] - 2020-6-15
### Changed
- fix bug AccessControl
- skip access_control

## [1.9.4] - 2020-6-15
### Changed
- change name

## [1.9.3] - 2020-6-15
### Changed
- fix bug

## [1.9.2] - 2020-6-15
### Changed
- change AccessControl verify

## [1.9.1] - 2020-6-15
### Changed
- change AccessControl verify
### Remove
- delete 1.9.0 version

## [1.9.0] - 2020-6-15
### Added
- add AccessControl verify
- add AccessControl register
### Remove
- permission_middleware

## [1.8.0] - 2020-3-22
### Added
- add ExceptionMiddleware

## [1.7.3] - 2020-2-24
### Changed
- Modify JWTMiddleware payload ['token '] type to str

## [1.7.2] - 2020-2-19
### Changed
- dingtalk: Support wechat message, text and markdown message types


## [1.7.1] - 2020-1-16
### Changed
- service_discovery: Compatible with services not registered to consumer

## [1.7.0] - 2020-1-10
### Added
- add ding_talk client
### Remove
- Remove the CacheManager and will not provide support in a future release

## [1.6.0] - 2020-1-08
### Added
- add service_log
### Changed
- ACL client can skip

## [1.5.1] - 2020-1-06
### Changed
- request_client and rest_client to optimize load balancing

## [1.5.0] - 2019-12-24
### Added
- ACL_MIDDLEWARE

## [1.4.13] - 2019-12-12
### Changed
- use queue name as rabbitmq consumer name

## [1.4.12] - 2019-12-10
### Changed
- changed rabbitmq connection default heartbeat

## [1.4.11] - 2019-12-03
### Added
- add aliyun amqp connection

## [1.4.10] - 2019-11-22
### Changed
- rest_client & requests_client add timeout

## [1.4.9] - 2019-11-19
### Changed
- rest_client & requests_client optimizer exception alert

## [1.4.8] - 2019-11-18
### Changed
- fix bug when sending subtask

## [1.4.7] - 2019-11-15
### Changed
- fix retry bug in rabbitmq_consumer
- fix retry bug in send_task

## [1.4.6] - 2019-11-11
### Changed
- rest_client and requests_client add auth retry

## [1.4.5] - 2019-11-08
### Changed
- message_sender add auto retry

## [1.4.4] - 2019-11-08
### Added
- add retry in function send_task 
- add retry in rabbitmq_consumer

## [1.3.3] - 2019-10-21
### Added
- service_configuration

## [1.2.3] - 2019-10-12
### Added
- schema command

### Changed
- Compatible with low version URL of Django 1.9
- Optimizing consul_service exception return

## [1.1.2] - 2019-09-19
### Changed
- rest_client requests_client add put 

## [1.1.1] - 2019-09-18
### Changed
- change table_api

## [1.1.0] - 2019-09-18
### Changed
- fix bug for api_permission middleware

## [1.0.9] - 2019-09-17
### Added
- table_api

### Changed
- fix bug for api_permission middleware
- service_discovery exception reminder add service name


## [1.0.8] - 2019-09-11
### Added
- requests_client

## [1.0.6] - 2019-09-11
### Added
- requests_client

### Changed
- restclient


## [1.0.5] - 2019-09-10
### Added
- rabbitmq_consumer


## [1.0.4] - 2019-09-06
### Added
- restclient
- message_client


## [1.0.3] - 2019-09-03
### Added


## [1.0.2] - 2019-09-03
### Added


## [1.0.1] - 2019-09-03
### Added


## [1.0.0] - 2019-09-03
### Added
- service_registry
- JWTMiddleware
- UserIDAuthentication
- API Permission Register
- METHOD_MIDDLEWARE
- PERMISSION_MIDDLEWARE