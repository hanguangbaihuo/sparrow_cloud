# from django.shortcuts import render
# from .models import CacheTest
# import uuid
# from rest_framework.response import Response
# from rest_framework.decorators import api_view

# @api_view(('GET',))
# def cachetest_detail(request, *args, **kwargs):
#     cache_test_obj = CacheTest.objects.create(id=uuid.uuid4().hex, name="CacheTest001")
#     cache_test_obj_g = CacheTest.objects.get(id=cache_test_obj.id)
#     return Response(cache_test_obj_g.name)