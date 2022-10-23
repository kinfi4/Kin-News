from django.core.management import BaseCommand

from api.views import container


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Starting the session...')
        container.clients.telegram_client().start_session()
