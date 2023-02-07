from django.core.management.base import BaseCommand

from server_app.enemies import EnemySpawnController
from time import sleep

class Command(BaseCommand):
    def add_arguments(self, parser):
        # parser.add_argument('--name', type=int)
        ...

    def handle(self, *args, **options):
        controller = EnemySpawnController()
        print('Enemy management daemon started')
        while True:
            controller.run()
            sleep(60)
