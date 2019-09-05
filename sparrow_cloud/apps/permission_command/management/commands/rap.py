from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        # disable logs of WARNING and below
        # import pdb; pdb.set_trace()
        print("suc")

