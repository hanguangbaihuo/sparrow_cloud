

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
    raise Exception("requests_client/rest_client build_url error: Address is not a string, address:{}".format(address))
