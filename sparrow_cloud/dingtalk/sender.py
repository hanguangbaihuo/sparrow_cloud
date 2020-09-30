import logging
from sparrow_cloud.restclient import rest_client
from sparrow_cloud.restclient.exception import HTTPException
from sparrow_cloud.utils.get_settings_value import get_settings_value

logger = logging.getLogger(__name__)


def send_message(msg, code_list, channel="dingtalk", message_type="text", *args, **kwargs):
    """钉钉群发消息机器人 client """
    if not isinstance(msg, str) and not isinstance(code_list, list):
        raise TypeError("参数类型错误：msg type not string or code_list type not list")
    data = {
        "msg": msg,
        "group_code_list": code_list,
        "channel": channel,
        "message_type": message_type
    }
    sparrow_ding_talk_conf = get_settings_value("SPARROW_DING_TALK_CONF")
    try:
        res = rest_client.post(sparrow_ding_talk_conf["SERVICE_DING_TALK"], sparrow_ding_talk_conf["PATH"], data=data, *args, **kwargs)
        logging.info("sparrow_cloud ding_talk send_message: msg:{}, group_code_list:{}".format(msg, code_list))
        return res
    except HTTPException as ex:
        logging.error("sparrow_cloud ding_talk send_message error: {}".format(ex))
        raise HTTPException(ex)
