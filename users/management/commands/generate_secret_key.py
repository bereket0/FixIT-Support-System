from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key


class Command(BaseCommand):
    help = 'Generate a secure secret key for Django'

    def handle(self, *args, **options):
        secret_key = get_random_secret_key()
        self.stdout.write(
            self.style.SUCCESS(f'Generated secret key: {secret_key}')
        )
        self.stdout.write(
            self.style.WARNING(
                'Add this to your environment variables as SECRET_KEY'
            )
        ) 