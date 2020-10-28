import logging
from sparrow_cloud.restclient import rest_client
from sparrow_cloud.restclient.exception import HTTPException
from sparrow_cloud.utils.get_cm_value import get_cm_value
logger = logging.getLogger(__name__)


def access_verify(user_id, app_name, resource_code):
    """
    access control verify
    """
    if all([user_id, app_name, resource_code]):
        sc_access_control_svc = get_cm_value("SC_ACCESS_CONTROL_SVC")
        sc_access_control_api = get_cm_value("SC_ACCESS_CONTROL_API")
        params = {
            "user_id": user_id,
            "app_name": app_name,
            "resource_code": resource_code
        }
        try:
            response = rest_client.get(sc_access_control_svc, api_path=sc_access_control_api, params=params)
            if response['has_perm']:
                return True
        except HTTPException as ex:
            if ex.status_code == 400 or ex.status_code == 403:
                logger.info("sparrow_cloud log : access verify failed. user:{}, message:{}".format(user_id, ex.detail))
                return False
            return True
    return False
