from django.shortcuts import render
from sparrow_cloud.registry.service_registry import consul_service
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


# Create your views here.

@api_view(('GET',))
def consul_service_demo(request):
    service_conf = {
        "service_name": "sparrow-permission-svc",  # k8s上的服务名称
        "host": "127.0.0.1:8001",  # 服务的真实host， 应用场景，consul服务故障， 或dev/test环境
    }
    try:
        service_addr = consul_service(service_conf)
    except:
        return Response({'message': '服务器错误'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({'service_addr': service_addr}, status=status.HTTP_200_OK)