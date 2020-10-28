import os


def get_cm_value(name):
    """get configmap value"""
    value = os.environ.get(name, None)
    if value is None:
        raise NotImplementedError("sparrow_cloud error：configmap not find:{}".format(name))
    return value