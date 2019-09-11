from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes


@api_view()
@permission_classes([AllowAny])
def table_api(request):


    return Response({"message": "ok"})

# app_lable, model, **kwargs