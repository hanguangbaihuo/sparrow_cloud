import logging
from sparrow_cloud.restclient import rest_client
from sparrow_cloud.restclient.exception import HTTPException
from sparrow_cloud.utils.get_cm_value import get_cm_value

logger = logging.getLogger(__name__)


def send_message(msg, code_list, channel="dingtalk", message_type="text", *args, **kwargs):
    """
        群发消息机器人 client
        configmap：
            SC_MESSAGE_ROBOT
            SC_MESSAGE_ROBOT_API
    """
    if not isinstance(msg, str) and not isinstance(code_list, list):
        raise TypeError("参数类型错误：msg type not string or code_list type not list")
    sc_message_robot = get_cm_value("SC_MESSAGE_ROBOT")
    sc_message_robot_api = get_cm_value("SC_MESSAGE_ROBOT_API")
    data = {
        "msg": msg,
        "group_code_list": code_list,
        "channel": channel,
        "message_type": message_type
    }
    try:
        res = rest_client.post(sc_message_robot, sc_message_robot_api, data=data, *args, **kwargs)
        logging.info("sparrow_cloud ding_talk send_message: msg:{}, group_code_list:{}".format(msg, code_list))
        return res
    except HTTPException as ex:
        logging.error("sparrow_cloud ding_talk send_message error: {}".format(ex))
        raise HTTPException(ex)
