

def build_url(protocol, address, api_path):
    """
    build_url
    :param protocol:  protocol
    :param address: address
    :param api_path: api path
    :return:
    """
    if isinstance(address, str):
        return "{}://{}{}".format(protocol, address, api_path)
