# import logging

# from django.core.management.base import BaseCommand

# from sparrow_cloud.restclient import rest_client
# from sparrow_cloud.utils.get_settings_value import get_settings_value
# from sparrow_cloud.utils.resource_cls_attribute import get_resource_cls

# logger = logging.getLogger(__name__)


# class Command(BaseCommand):
#     help = '注册访问控制code'

#     def handle(self, *args, **options):
#         """
#         access control register
#         """
#         app_name = get_settings_value("SERVICE_CONF").get("NAME", None)
#         secret = get_settings_value("ACCESS_CONTROL").get("SECRET", None)
#         api_path = get_settings_value("ACCESS_CONTROL").get("REGISTER_API_PATH", None)
#         service_conf = get_settings_value("ACCESS_CONTROL").get("ACCESS_CONTROL_SERVICE", None)
#         access_control_class_path = get_settings_value("ACCESS_CONTROL").get("ACCESS_CONTROL_CLASS", None)
#         if all([access_control_class_path, app_name, secret, service_conf]):
#             access_control_cls = get_resource_cls()
#             attribute_name_list = [_ for _ in dir(access_control_cls) if _.startswith('permission_')]
#             data = [getattr(access_control_cls, _) for _ in attribute_name_list]
#             payload = {
#                 "app_name": app_name,
#                 "secret": secret,
#                 "data": data
#             }
#             try:
#                 rest_client.post(service_conf, api_path=api_path, json=payload)
#                 print("resource register success!!!")
#             except Exception as ex:
#                 print("resource register failed, message:{}".format(ex.__str__()))