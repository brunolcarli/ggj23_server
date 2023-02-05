from django.core.management.base import BaseCommand

from server_app.enemies import enemies_spawned
from server_app.map_areas import areas
from time import sleep

class Command(BaseCommand):
    def add_arguments(self, parser):
        # parser.add_argument('--name', type=int)
        ...

    def handle(self, *args, **options):
        print('Enemy management daemon started')
        while True:
            enemies_spawned.manage_enemies()
            sleep(2)