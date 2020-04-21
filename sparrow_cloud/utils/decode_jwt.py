import jwt
from sparrow_cloud.utils.get_settings_value import get_settings_value


def get_jwt_secret():
    jwt_conf = get_settings_value("JWT_MIDDLEWARE")
    return jwt_conf["JWT_SECRET"]


def decode_jwt(token):
    secret = get_jwt_secret()
    try:
        payload = jwt.decode(token, secret, algorithms='HS256')
    except Exception as ex:
        raise ex
    return payload

