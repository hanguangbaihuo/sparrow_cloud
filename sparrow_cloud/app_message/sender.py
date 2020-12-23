import logging
from sparrow_cloud.restclient import rest_client
from sparrow_cloud.restclient.exception import HTTPException
from sparrow_cloud.utils.get_cm_value import get_cm_value
from sparrow_cloud.utils.get_settings_value import get_service_name

logger = logging.getLogger(__name__)


def send_message(msg_data, code_type, content_type="text", msg_sender=None, *args, **kwargs):
    """
        # ConfigMap:
            SC_LY_MESSAGE
            SC_LY_MESSAGE_API
    """
    if msg_sender is None:
        msg_sender = get_service_name()
    sc_ly_message = get_cm_value("SC_LY_MESSAGE")
    sc_ly_message_api = get_cm_value("SC_LY_MESSAGE_API")
    data = {
        "shop_id": kwargs.pop("shop_id", ""),
        "msg_sender": msg_sender,
        "code_type": code_type,
        "msg": {
            "content_type": content_type,
            "data": msg_data
        }
    }
    try:
        res = rest_client.post(sc_ly_message, sc_ly_message_api, json=data, *args, **kwargs)
        logging.info("sparrow_cloud ly_message send_message, data:{}, code_type:{}".format(data, code_type))
        return res
    except HTTPException as ex:
        logging.error("sparrow_cloud ly_message send_message error: {}".format(ex))
        raise HTTPException(ex)
