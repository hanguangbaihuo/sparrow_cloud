import os


def get_cm_value(name):
    """get configmap value"""
    value = os.environ.get(name, None)
    if value is None:
        raise NotImplementedError("sparrow_cloud error：configmap not find:{}".format(name))
    return value

def get_env_value(name):
    '''get environment value or none'''
    return os.environ.get(name, None)