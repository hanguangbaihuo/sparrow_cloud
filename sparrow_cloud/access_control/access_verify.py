import logging
from sparrow_cloud.restclient import rest_client
from sparrow_cloud.restclient.exception import HTTPException
from sparrow_cloud.utils.get_settings_value import get_settings_value
logger = logging.getLogger(__name__)


def access_verify(user_id, app_name, resource_code):
    """
    ACCESS_CONTROL = {
        "ACCESS_CONTROL_SERVICE": {
            "ENV_NAME": "HOST",
            "VALUE": os.environ.get("", ""),
        },
        "VERIFY_API_PATH": "verify_api_path",
        "REGISTER_API_PATH": "register_api_path",
        "ACCESS_CONTROL_CLASS": "your.PromotionAccessControl.path",
        "SECRET": "secret"
    }

    """
    if all([user_id, app_name, resource_code]):
        service_conf = get_settings_value("ACCESS_CONTROL").get("ACCESS_CONTROL_SERVICE")
        api_path = get_settings_value("ACCESS_CONTROL").get("VERIFY_API_PATH")
        params = {
            "user_id": user_id,
            "app_name": app_name,
            "resource_code": resource_code
        }
        try:
            response = rest_client.get(service_conf, api_path=api_path, timeout=0.5, params=params)
            if response['has_perm']:
                return True
            else:
                logger.info("sparrow_cloud log : access verify failed. user:{}".format(user_id))
                return False
        except HTTPException as ex:
            if ex.status_code == 400:
                return False
            raise ex
    return False
