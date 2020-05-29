from sparrow_cloud.access_control.base_access_control import BaseAccessControl


class ExampleAccessControl(BaseAccessControl):
    """访问控制资源
        每个资源由用字典组成:
            名称规范: 资源名称需要以permission_开头， 否则不会注册, 例如: permission_Example1
            资源key必须为: resource_code
            资源描述key必须为: desc
            示例:
                permission_test1 = {
                    "resource_code": "自定义的访问控制资源",
                    "desc": "描述"
                }
    """
    permission_example1 = {
        "resource_code": "example1_admin",
        "desc": "描述"
    }
    permission_example2 = {
        "resource_code": "example2_admin",
        "desc": "描述"
    }
    permission_example3 = {
        "resource_code": "example3_admin",
        "desc": "描述"
    }
