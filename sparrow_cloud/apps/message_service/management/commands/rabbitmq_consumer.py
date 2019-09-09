from django.core.management.base import BaseCommand
from ._sparrow_rabbitmq_consumer import rabbitmq_consumer
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'sparrow_rabbitmq_consumer'

    def add_arguments(self, parser):
        parser.add_argument('--queue', dest="queue", default='', type=str)

    def handle(self, *args, **kwargs):
        queue = kwargs.get('queue', None)
        if queue:
            rabbitmq_consumer(queue=queue)
        else:
            logger.error('请在调用命令时传入参数：--queue')
            print('请在调用命令时传入参数：--queue')




