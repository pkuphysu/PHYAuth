from django.core.management.base import BaseCommand
from ...models import Iaaa


class Command(BaseCommand):
    help = 'Create iaaa app info.'

    def handle(self, *args, **options):
        try:
            app_id = input('Please input the appID: ')
            if app_id == '':
                raise ValueError('app id can not be empty!')
            key = input('Please input the appKEY: ')
            if key == '':
                raise ValueError('app key can not be empty!')
            redirect_url = input('Please inputh the redirect_url: ')
            if redirect_url == '':
                raise ValueError('redirect_url can not be empty!')
            if not redirect_url.startswith('http'):
                raise ValueError('redirect_url should start with http!')
            Iaaa.objects.create(app_id=app_id, key=key, redirect_url=redirect_url)
            self.stdout.write(self.style.SUCCESS('IAAA app successfully created.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Something goes wrong: {0}'.format(e)))
