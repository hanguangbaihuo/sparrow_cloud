from rest_framework.views import APIView

from .generators import SchemaGenerator
from .inspectors import AutoSchema, DefaultSchema, ManualSchema
# 为APIView添加schema描述对象
setattr(APIView, "schema", DefaultSchema())

