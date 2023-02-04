from django.core.management.base import BaseCommand

from server_app.enemies import manage_enemies
from server_app.map_areas import areas
from time import sleep

class Command(BaseCommand):
    def add_arguments(self, parser):
        # parser.add_argument('--name', type=int)
        ...

    def handle(self, *args, **options):
        print('Enemy management daemon started')
        enemies_spawned = {a: [] for a in areas}
        while True:
            manage_enemies(enemies_spawned)
            sleep(2)