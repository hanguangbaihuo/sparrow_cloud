import logging
import traceback
from django.conf import settings
from sparrow_cloud.dingtalk.sender import send_message
from sparrow_cloud.middleware.base.base_middleware import MiddlewareMixin

logger = logging.getLogger(__name__)


MESSAGE_LINE = """
##### <font color=\"info\"> 服务名称: {service_name}</font> #####
> 进程异常message:<font color=\"warning\">{exception_info}</font>
"""


class ExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        debug = settings.DEBUG
        code = getattr(settings, "CLOUD_ERROR_NOTIFICATION_ROBOT", "cloud_error_notification_robot")
        service_name = getattr(settings, "SERVICE_CONF", None).get("NAME", None)
        if debug is True:
            pass
        else:
            exception_info = traceback.format_exc()[-800:-1]
            try:
                msg = MESSAGE_LINE.format(service_name=service_name, exception_info=exception_info)
                logger.info("sparrow_cloud log, service process_exception info : {}".format(msg))
                send_message(msg=msg, code_list=[code], channel="wechat", message_type="markdown")
            except Exception as ex:
                logger.error("sparrow_cloud 发送服务异常信息通知失败，原因: {}".format(ex))