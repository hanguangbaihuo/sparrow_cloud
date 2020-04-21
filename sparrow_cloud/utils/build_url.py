from sparrow_cloud.registry.service_discovery import load_balance_address


def build_url(address_list, api_path):
    """
    build_url
    :param address_list:  service conf
    :param api_path: api path
    :return:
    """
    if isinstance(address_list, str):
        return "http://{}{}".format(address_list, api_path), address_list
    address = load_balance_address(address_list)
    host = address['ServiceAddress']
    port = address['ServicePort']
    domain = "{host}:{port}".format(host=host, port=port)
    return "http://{}{}".format(domain, api_path), address
