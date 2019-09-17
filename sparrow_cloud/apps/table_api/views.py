from rest_framework import status, generics
from django.apps import apps
from .serializers import TableSerializer
from rest_framework.response import Response


class TableView(generics.ListAPIView):
    serializer_class = TableSerializer

    def list(self, request, *args, **kwargs):
        app_lable = self.request.data.get('app_lable', None)
        model = self.request.data.get('model', None)
        filter_condition = self.request.data.get('filter_condition', None)
        if (app_lable and model and filter_condition) is None:
            return Response({'code': 1, 'message': '参数不全，请检查参数：app_lable/model/filter_condition'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            model = apps.get_model(app_lable, model)
            data = model.objects.filter(**filter_condition)
            TableSerializer.Meta.model = model
            serializer = self.get_serializer(data, many=True)
            result = {'code': 0, 'message': 'ok', 'data': serializer.data}
            return Response(result, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'code': 1, "message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

