from django.core.management.base import BaseCommand
from ._sparrow_rabbitmq_consumer import rabbitmq_consumer
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'sparrow_rabbitmq_consumer'

    def add_arguments(self, parser):
        parser.add_argument('--queue', dest="queue", default='', type=str)

    def handle(self, *args, **kwargs):
        queue = kwargs['queue']
        if queue:
            try:
                # import pdb;pdb.set_trace()
                rabbitmq_consumer(queue=queue)
            except Exception as ex:
                logger.error(ex)
