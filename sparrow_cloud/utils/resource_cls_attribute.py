# import logging
# import importlib
# from sparrow_cloud.utils.common_exceptions import ResourceValidError
# from sparrow_cloud.utils.get_settings_value import get_settings_value


# def get_resource_cls():
#     """
#     get resource class
#     """
#     access_control_class = get_settings_value("ACCESS_CONTROL").get("ACCESS_CONTROL_CLASS", None)
#     if access_control_class:
#         try:
#             module_path, cls_name = access_control_class.rsplit(".", 1)
#             resource_cls = getattr(importlib.import_module(module_path), cls_name)
#         except Exception as ex:
#             raise ResourceValidError('ACCESS_CONTROL ERROR: ACCESS_CONTROL_CLASS ，MESSAGE:{}'.format(ex.__str__()))
#         return resource_cls
#     raise ResourceValidError('ACCESS_CONTROL ERROR: ACCESS_CONTROL_CLASS not configured.')



