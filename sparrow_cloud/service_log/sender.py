import logging
from sparrow_cloud.restclient.rest_client import post
from sparrow_cloud.restclient.exception import HTTPException
from sparrow_cloud.utils.get_settings_value import get_settings_value
logger = logging.getLogger(__name__)


def send_log(data):
    """
    SPARROW_SERVICE_LOG_CONF = {
    "SERVICE_LOG": {
            "ENV_NAME": "SPARROW_SERVICE_LOG",
            "VALUE": os.environ.get("SPARROW_SERVICE_LOG", "sparrow-service-log-svc"),
        },
        "PATH": "/service_log/log/",
    }

    :param data: dict
    :return:True, False
    """
    service_conf = get_settings_value("SERVICE_CONF")
    service_log_conf = get_settings_value("SPARROW_SERVICE_LOG_CONF")
    data["service_name"] = service_conf["NAME"]
    try:
        response = post(service_log_conf["SERVICE_LOG"], service_log_conf["PATH"], data=data)
        logging.info("sparrow_cloud: service log sent successfully, message:{}".format(response))
        return True
    except HTTPException as ex:
        logging.info("sparrow_cloud: Service log sending failed, message:{}".format(ex.__str__()))
        return False
