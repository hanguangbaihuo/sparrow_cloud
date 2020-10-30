import logging
from sparrow_cloud.restclient.rest_client import post
from sparrow_cloud.restclient.exception import HTTPException
from sparrow_cloud.utils.get_settings_value import get_service_name
from sparrow_cloud.utils.get_cm_value import get_cm_value
logger = logging.getLogger(__name__)


def send_log(data):
    """
    :param data: dict
    :return:True, False
    """
    if not isinstance(data, dict):
        raise TypeError("参数类型错误：except=%s, get=%s" % ("dict", type(data)))
    data["service_name"] = get_service_name()
    service_log_svc = get_cm_value("SC_SERVICE_LOG_SVC")
    service_log_api = get_cm_value("SC_SERVICE_LOG_API")
    try:
        response = post(service_log_svc, service_log_api, data=data)
        logging.info("sparrow_cloud: service log sent successfully, message:{}".format(response))
        return True
    except HTTPException as ex:
        logging.error("sparrow_cloud: Service log sending failed, message:{}".format(ex.__str__()))
        return False
