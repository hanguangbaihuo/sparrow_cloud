import jwt

from sparrow_cloud.utils.get_settings_value import GetSettingsValue


class DecodeJwt(object):
    """decode_jwt"""

    def __init__(self, ):
        self.settings_value = GetSettingsValue()
        self.secret = self.settings_value.get_middleware_value(
            'JWT_MIDDLEWARE', 'JWT_SECRET')

    def decode_jwt(self, token):
        secret = self.secret
        try:
            payload = jwt.decode(token, secret, algorithms='HS256')
        except Exception as ex:
            raise ex
        return payload
