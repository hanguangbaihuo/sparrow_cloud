from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


@api_view()
# @permission_classes([IsAuthenticated])
def ping(request):
    # import pdb; pdb.set_trace() 
    return Response({
        "message": "ok"
    })