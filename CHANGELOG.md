# Changelog
此项目的所有显着更改都将记录在此文件中。


格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [Unreleased]
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