import jwt
import os
from sparrow_cloud.utils.get_cm_value import get_env_value
from sparrow_cloud.utils.get_settings_value import get_settings_value


def get_jwt_secret():
    return get_env_value("JWT_SECRET") or get_settings_value("JWT_MIDDLEWARE").get("JWT_SECRET")


def decode_jwt(token):
    secret = get_jwt_secret()
    try:
        payload = jwt.decode(token, secret, algorithms='HS256')
    except Exception as ex:
        raise ex
    return payload

