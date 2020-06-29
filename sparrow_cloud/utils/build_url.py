

def build_url(address, api_path):
    """
    build_url
    :param address_list:  service conf
    :param api_path: api path
    :return:
    """
    if isinstance(address, str):
        return "http://{}{}".format(address, api_path)
