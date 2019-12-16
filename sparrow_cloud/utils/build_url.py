from sparrow_cloud.registry.service_discovery import consul_service


def build_url(service_conf, api_path):
    """
    build_url
    :param service_conf:  service conf
    :param api_path: api path
    :return:
    """
    servicer_addr = consul_service(service_conf)
    return "http://{}{}".format(servicer_addr, api_path)