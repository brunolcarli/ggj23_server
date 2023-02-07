from base64 import b64encode
import uuid
import json
import requests
from django.conf import settings
from random import choice, random
from server_app.skills import skill_list
from server_app.map_areas import areas
from server_app.engine import target_position_is_valid
from server_app.models import Character, SpawnedEnemy
from ggj23.settings import REDIS_HOST, REDIS_PORT
from redis import Redis
from server_app.serializer import Serializer
from server_app.events import OnCharacterEvent

enemies_spots = {
    'citadel': [],
    'open_fields': ['spider', 'goblin', 'wolf'],
    'yggdrasil': ['orc', 'ent', 'poison_snake', 'spirit', 'bear', 'killer_fungus',  'golem'],
    'combat_zone': [],
    'ancient_forest_area1': ['spider', 'goblin'],
    'ancient_forest_area2': ['spider', 'killer_fungus'],
    'ancient_forest_area3': ['ent', 'poison_snake', 'killer_fungus'],
    'ancient_forest_elder_cave': ['spider', 'goblin', 'wolf', 'ent'],
    'ancient_forest_village': [],
    'vulcanic_zone_area1': ['spider', 'goblin'],
    'vulcanic_zone_area2': ['goblin', 'wolf'],
    'vulcanic_zone_area3': ['goblin', 'wolf', 'poison_snake'],
    'vulcanic_zone_elder_cave': ['goblin', 'wolf', 'orc', 'poison_snake'],
    'vulcanic_zone_village': [],
    'snowfields_area1': ['goblin', 'wolf'],
    'snowfields_area2': ['wolf', 'bear'],
    'snowfields_area3': ['wolf', 'orc'],
    'snowfields_elder_cave': ['wolf', 'orc', 'spirit', 'bear'],
    'snowfields_village': [],
    'chrono_mountains_area1': ['spider', 'goblin', 'wolf'],
    'chrono_mountains_area2': ['goblin', 'wolf', 'bear'],
    'chrono_mountains_area3': ['goblin', 'wolf', 'orc'],
    'chrono_mountains_elder_cave': ['goblin', 'wolf', 'orc', 'poison_snake'],
    'chrono_mountains_village': []
}


enemy_list = {
    'spider': {
        'lv': 1,
        'name': 'spider',
        'hp': 50,
        'power': 10,
        'resistance': 5,
        'agility': 1,
        'aim': 80,
        'class_type': 'enemy',
        'exp': 3,
        'drops': [],
        'skills': [skill_list['base_attack']]
    },
    'goblin': {
        'lv': 1,
        'name': 'goblin',
        'hp': 80,
        'power': 13,
        'resistance': 5,
        'agility': 1,
        'aim': 70,
        'class_type': 'enemy',
        'exp': 5,
        'drops': [],
        'skills': [
            skill_list['base_attack'],
            skill_list['fireball']
        ],
    },
    'wolf': {
        'lv': 1,
        'name': 'wolf',
        'hp': 70,
        'power': 15,
        'resistance': 6,
        'agility': 1,
        'aim': 80,
        'class_type': 'enemy',
        'exp': 6,
        'drops': [],
        'skills': [
            skill_list['base_attack'],
            skill_list['fireball']
        ],
    },
    'orc': {
        'lv': 2,
        'name': 'orc',
        'hp': 100,
        'power': 19,
        'resistance': 9,
        'agility': 1,
        'aim': 80,
        'class_type': 'enemy',
        'exp': 12,
        'drops': [],
        'skills': [
            skill_list['base_attack'],
            skill_list['ice_lance'],
            skill_list['air_cutter']
        ],
    },
    'poison_snake': {
        'lv': 2,
        'name': 'poison_snake',
        'hp': 80,
        'power': 16,
        'resistance': 7,
        'agility': 1,
        'aim': 80,
        'class_type': 'enemy',
        'exp': 9,
        'drops': [],
        'skills': [
            skill_list['base_attack'],
            skill_list['eruption']
        ],
    },
    'ent': {
        'lv': 3,
        'name': 'ent',
        'hp': 150,
        'power': 23,
        'resistance': 25,
        'agility': 1,
        'aim': 80,
        'class_type': 'enemy',
        'exp': 16,
        'drops': [],
        'skills': [
            skill_list['base_attack'],
            skill_list['air_cutter'],
            skill_list['windstorm']
        ],
    },
    'spirit': {
        'lv': 3,
        'name': 'spirit',
        'hp': 200,
        'power': 20,
        'resistance': 20,
        'agility': 1,
        'aim': 80,
        'class_type': 'enemy',
        'exp': 20,
        'drops': [],
        'skills': [
            skill_list['base_attack'],
            skill_list['fireball'],
            skill_list['eruption'],
            skill_list['windstorm'],
            skill_list['air_cutter']
        ],
    },
    'bear': {
        'lv': 4,
        'name': 'bear',
        'hp': 350,
        'power': 40,
        'resistance': 25,
        'agility': 1,
        'aim': 80,
        'class_type': 'enemy',
        'exp': 33,
        'drops': [],
        'skills': [
            skill_list['base_attack'],
            skill_list['eruption'],
            skill_list['air_cutter']
        ],
    },
    'killer_fungus': {
        'lv': 4,
        'name': 'killer_fungus',
        'hp': 250,
        'power': 19,
        'resistance': 25,
        'agility': 1,
        'aim': 80,
        'class_type': 'enemy',
        'exp': 26,
        'drops': [],
        'skills': [
            skill_list['base_attack'],
            skill_list['windstorm'],
            skill_list['blind'],
            skill_list['enemy_down']
        ],
    },
    'golem': {
        'lv': 5,
        'name': 'golem',
        'hp': 500,
        'power': 40,
        'resistance': 70,
        'agility': 1,
        'aim': 80,
        'class_type': 'enemy',
        'exp': 100,
        'drops': [],
        'skills': [
            skill_list['base_attack'],
            skill_list['rock_throw'],
            skill_list['eruption']
        ],
    },
}


class EnemySpawnController:
    """
    Handle enemy monster spawning.
    """
    def __init__(self):
        self.spawn_rate = settings.GAME_CONFIG['SPAWN_RATE']
        self.max_enemies = settings.GAME_CONFIG['MAX_ENEMIES_PER_AREA']

    def _get_possible_pixel(self, area_max):
        return choice([28*i for i in range(1, (area_max//28)+1)])

    def spawn(self):
        """
        Main spawn controller runner.
        Checks if is possible to spawn a new monster in an area.
        The spawn is considered an character_event.
        When a new enemy spawns, the controller broadcasts the event
        to all connected clients.
        """
        # Handle spawnin in each game area
        for area in areas:
            # Ignore spawning if area already reached max enemy count
            spawned_count = SpawnedEnemy.objects.filter(area_location=area).count()
            if spawned_count == self.max_enemies:
                continue

            # Get possible enemy kinds that appear in the iterated area
            possible_enemies = enemies_spots[area]

            # Ignore spawning if area ont have enemies (like cities and villages)
            if not possible_enemies:
                continue

            # Calculate chance of enemy spawn
            if random() > self.spawn_rate:
                continue

            # randomly select an possible enemy to spawn
            enemy_type = enemy_list[choice(possible_enemies)]

            # Creates a new atabase record for spawned enemy
            enemy = SpawnedEnemy(
                lv=enemy_type['lv'],
                name=enemy_type['name'],
                max_hp=enemy_type['hp'],
                current_hp=enemy_type['hp'],
                power=enemy_type['power'],
                resistance=enemy_type['resistance'],
                agility=enemy_type['agility'],
                aim=enemy_type['aim'],
                exp=enemy_type['exp'],
                drops=json.dumps(enemy_type['drops']).encode('utf-8'),
                skills=json.dumps(enemy_type['skills']).encode('utf-8'),
                area_location=area,
                effects=b'[]',
                position_x = self._get_possible_pixel(areas[area]['size_x']),
                position_y = self._get_possible_pixel(areas[area]['size_y'])
            )
            enemy.save()

            # Broadcast enemy spawning
            payload = {
                'enemy_id': enemy.id,
                'enemy_name': enemy.name,
                'position_x': enemy.position_x,
                'position_y': enemy.position_y,
                'area': area
            }
            query = f'''
                mutation{{
                    notifyEnemyEvent(input:{{
                        eventType: "enemy_spawn"
                        data: "{b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8')}"
                    }}){{
                    result
                    }}
                }}
            '''
            requests.post(
                settings.GQL_URL,
                json={'query': query}
            )

    def move(self):
        """
        Move an enemy randomly
        """
        directions = ['up', 'down', 'left', 'right', 'none']
        for mob in SpawnedEnemy.objects.all():
            move_to = choice(directions)

            current_x, current_y = mob.position_x, mob.position_y
            if move_to == 'up':
                mob.position_y -= 28
            elif move_to == 'down':
                mob.position_y += 28
            elif move_to == 'right':
                mob.position_x += 28
            elif move_to == 'left':
                mob.position_x -= 28
            else:
                continue

            if not target_position_is_valid([mob.position_x, mob.position_y], mob.area_location):
                mob.position_x = current_x
                mob.position_y = current_y
                mob.save()
                continue
            mob.save()

            # Broadcast enemy movement
            payload = {
                'enemy_id': mob.id,
                'enemy_name': mob.name,
                'position_x': mob.position_x,
                'position_y': mob.position_y,
                'area': mob.area_location
            }
            query = f'''
                mutation{{
                    notifyEnemyEvent(input:{{
                        eventType: "enemy_movement"
                        data: "{b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8')}"
                    }}){{
                    result
                    }}
                }}
            '''
            requests.post(
                settings.GQL_URL,
                json={'query': query}
            )
