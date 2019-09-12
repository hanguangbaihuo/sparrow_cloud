from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.apps import apps


@api_view()
@permission_classes([AllowAny])
def table_api(request, *args, **kwargs):
    app_lable = kwargs.get('app_lable')
    model = kwargs.get('model')
    data = kwargs.get('data')
    try:
        model = apps.get_model(app_lable, model)
        data = model.objects.filter(data)

    except Exception as ex:
        return Response({"message": str(ex)})
    return Response({"message": "ok"})

