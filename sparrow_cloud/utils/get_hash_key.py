import hashlib
from django.conf import settings


def get_hash_key():
    """
    根据settings的SECRET_KEY，生成acl_token_key
    acl_token_key 生成方式:
        ACL_TOKEN +（SECRET_KEY md5 加密后的前6位）
    """
    secret_key = getattr(settings, 'SECRET_KEY', '')
    md = hashlib.md5()
    md.update(secret_key.encode('utf-8'))
    key = "ACL_TOKEN" + '_' + (md.hexdigest()[:7]).upper()
    return key
