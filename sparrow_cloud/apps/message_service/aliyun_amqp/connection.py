# -*- coding: utf-8 -*
import pika
from .AliyunCredentialsProvider3 import AliyunCredentialsProvider

#接入点
# 公网   20882320.mq-amqp.cn-beijing-a.aliyuncs.com
# 内外地址 20882320.mq-amqp.cn-beijing-a-internal.aliyuncs.com
host = "20882320.mq-amqp.cn-beijing-a.aliyuncs.com"
#默认端口
port = 5672
#资源隔离
virtualHost = "sparrow_test"
#阿里云的accessKey
accessKey = "LTAI4FirPhTQuA5tYfY2JLEv"
#阿里云的accessSecret
accessSecret = "xKvX9tWe8wkYmxwkaMiXL1LIe8hdq1"
#主账号id
resourceOwnerId = 20882320
security_token = ""

provider = AliyunCredentialsProvider(accessKey, accessSecret, resourceOwnerId)

def getConnectionParam():
    credentials = pika.PlainCredentials(provider.get_username(), provider.get_password(), erase_on_connect=True)
    return pika.ConnectionParameters(host, port, virtualHost, credentials)