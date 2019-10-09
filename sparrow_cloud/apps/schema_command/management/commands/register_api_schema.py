import json
from django.core.management.base import BaseCommand
from sparrow_cloud.apps.schema_command.schemas.generators import SchemaGenerator


class Command(BaseCommand):
    help = "注册api schema到文档中心"

    def add_arguments(self, parser):
        parser.add_argument(
            '-p', '--print',
            default=False, action="store_true",
            help='打印api schema 到控制台'
        )

    def handle(self, *args, **options):
        import pdb
        pdb.set_trace()
        print(options)
        sg = SchemaGenerator()
        schema = sg.get_schema_dict()
        # print(schema)
        data = json.dumps(schema, ensure_ascii=False)
        if options["print"] is True:
            print(data)
        return data

