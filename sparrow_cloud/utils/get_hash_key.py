import hashlib
from sparrow_cloud.utils.get_settings_value import get_settings_value


def get_hash_key(key_type, user_id=None):
    """
    根据settings的SECRET_KEY，生成app_hash_key/user_hash_key
    app_token_key 生成方式:
        ACL_TOKEN +（SECRET_KEY md5 加密后的前6位）
    """
    if key_type == "app":
        secret_key = get_settings_value(name="SERVICE_CONF")["SECRET"]
        return "APP_TOKEN" + '_' + md5_key(secret_key)
    if key_type == "user":
        secret_key = user_id
        return "USER_TOKEN" + '_' + md5_key(secret_key)


def md5_key(secret):
    md = hashlib.md5()
    md.update(secret.encode('utf-8'))
    return (md.hexdigest()[:7]).upper()
