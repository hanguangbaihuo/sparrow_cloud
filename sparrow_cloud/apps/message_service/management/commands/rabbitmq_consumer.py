from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'sparrow_rabbitmq_consumer'

    def handle(self, *args, **kwargs):

        print("sparrow_rabbitmq_consumer")

