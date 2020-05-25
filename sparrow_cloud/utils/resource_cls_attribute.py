import logging
import importlib
from sparrow_cloud.utils.common_exceptions import ResourceValidError


def get_resource_cls_attribute(resource=None):
    if resource:
        attribute, module_path, cls_name = resource.rsplit(".", 2)
        try:
            resource_cls = getattr(importlib.import_module(module_path), cls_name)
        except Exception as ex:
            logging.error('ERROR: access_control incorrect incoming parameters,'
                          'resource:{}, message:{},'.format(resource, ex.__str__()))
            raise ResourceValidError('ERROR: access_control incorrect incoming parameters, '
                                     'resource:{}, message:{},'.format(resource, str(ex)))
        return resource_cls.attribute
