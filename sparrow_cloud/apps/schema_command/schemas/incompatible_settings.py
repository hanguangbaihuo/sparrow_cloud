"""
    drf 不兼容的配置项
"""
SCHEMA_COERCE_METHOD_NAMES = {
    'retrieve': 'read',
    'destroy': 'delete'
}
SCHEMA_COERCE_PATH_PK = True
