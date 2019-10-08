

def set_up():
    import os
    import django
    print(django.__version__)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hg_backend.settings")
    os.environ.setdefault("RUN_ENV", "unit")
    django.setup()


if __name__ == "__main__":
    set_up()
    from ..schemas.generators import SchemaGenerator
    from rest_framework.views import APIView
    from ..schemas.inspectors import DefaultSchema
    from ..schemas import patch
    # print(APIView.schema)
    # from rest_framework.schemas import SchemaGenerator
    sg = SchemaGenerator()
    import json
    _sg = sg.get_schema_dict()
    print(json.dumps(_sg, ensure_ascii=False))


