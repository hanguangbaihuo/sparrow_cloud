#!/bin/bash

#  message_client配置
export SC_MESSAGE_SENDER_SVC=task-test-svc:8080
export SC_MESSAGE_SENDER_API=/api/task/send/
# rabbitmq 环境变量设置
export SC_BROKER_USERNAME=test
export SC_BROKER_PASSWORD=test
export SC_BROKER_VIRTUAL_HOST=test
export SC_BROKER_SERVICE_HOST=rabbitmq
export SC_BROKER_SERVICE_PORT=666
export SC_BACKEND_SERVICE_SVC=task-svc:8080
export SC_BACKEND_SERVICE_API=/api/task/task/update/
export SC_CONSUMER_RETRY_TIMES=3
export SC_CONSUMER_INTERVAL_TIME=3
export SC_CONSUMER_HEARTBEAT=600
# 文档注册
export SC_SCHEMA_SVC=schema-svc:8080
export SC_SCHEMA_API=/api/schema/register/
#  发送机器人消息
export SC_MESSAGE_ROBOT=dingtalk-robot-svc:8080
export SC_MESSAGE_ROBOT_API=/api/robot/warning_message/
# 访问控制的配置
export SC_ACCESS_CONTROL_SVC=access-control-svc:8080
export SC_ACCESS_CONTROL_API=/api/ac/verify/
# get_user_token&get_app_token
export SC_MANAGE_SVC=app-manage-svc:8080
export SC_MANAGE_API=/api/apps/login
# 兼容阿里不支持put delete, django中间件
export SC_METHOD_MAP='{"PUT"="PUT", "DELETE"="DELETE"}'
# go 语言task代理客户端 
export SC_TASK_PROXY=TASK_PROXY_SVC
export SC_TASK_PROXY_API=/api/task_proxy/producer/send