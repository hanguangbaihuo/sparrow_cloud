from rest_framework.views import APIView
from .inspectors import DefaultSchema


# 改变drf默认的 ApiView类的schema属性
def patch_apiview_schema():
    # 为APIView添加schema描述对象
    setattr(APIView, "schema", DefaultSchema())


patch_apiview_schema()


