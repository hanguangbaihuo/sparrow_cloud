from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


@api_view(("GET", "POST", "DELETE", "PUT"))
# @permission_classes([IsAuthenticated])
def test_path_params_1(request):
    # import pdb; pdb.set_trace() 
    return Response({
        "message": "ok"
    })



@api_view(("GET", "POST", "DELETE", "PUT"))
# @permission_classes([IsAuthenticated])
def test_path_params_2(request):
    # import pdb; pdb.set_trace() 
    return Response({
        "message": "ok"
    })


@api_view(("GET", ))
# @permission_classes([IsAuthenticated])
def test_path_no_params_2(request):
    # import pdb; pdb.set_trace() 
    return Response({
        "message": "ok"
    })


@api_view(("GET", ))
# @permission_classes([IsAuthenticated])
def test_path_no_params_1(request):
    # import pdb; pdb.set_trace() 
    return Response({
        "message": "ok"
    })