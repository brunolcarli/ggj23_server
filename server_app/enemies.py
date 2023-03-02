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
from server_app.serializer import Serializer
from server_app.events import OnCharacterEvent


enemies_spots = {
    # 'citadel_central_area': [],
    # 'citadel_north_area': [],
    # 'citadel_south_area': [],
    # 'citadel_east_area': [],
    # 'citadel_west_area': [],
    'open_fields_area1': {
        'spider': [(4, 21), (15, 29), (20, 27), (20, 11), (8, 9), (18, 46)],
        'goblin': [(15, 14), (19, 17), (14, 24), (15, 30), (21, 6), (35, 44)],
        'wolf': [(15, 19), (6, 9), (15, 12), (20, 25), (30, 17), (29, 42)]
    },
    # 'open_fields_area2': {
    #     'spider': [(4, 21), (15, 29), (20, 27), (20, 11), (8, 9), (18, 46)],
    #     'goblin': [(15, 14), (19, 17), (14, 24), (15, 30), (21, 6), (35, 44)],
    #     'wolf': [(15, 19), (6, 9), (15, 12), (20, 25), (30, 17), (29, 42)]
    # },
    # 'open_fields_area3': ['spider', 'goblin', 'wolf'],
    # 'open_fields_area4': ['spider', 'goblin', 'wolf'],
    # 'open_fields_area5': ['spider', 'goblin', 'wolf'],
    # 'open_fields_area6': ['spider', 'goblin', 'wolf'],
    # 'open_fields_area7': ['spider', 'goblin', 'wolf'],
    # 'open_fields_area8': ['spider', 'goblin', 'wolf'],
    # 'open_fields_area9': ['spider', 'goblin', 'wolf'],
    # 'open_fields_area10': ['spider', 'goblin', 'wolf'],
    # 'open_fields_area11': ['spider', 'goblin', 'wolf'],
    # 'open_fields_area12': ['spider', 'goblin', 'wolf'],
    'open_fields_area13': {
        'spider': [(4, 21), (15, 29), (20, 27), (20, 11), (8, 9)],
        'goblin': [(15, 14), (19, 17), (14, 24), (15, 30), (21, 6)],
        'wolf': [(15, 19), (6, 9), (15, 12), (20, 25)]
    },
    'open_fields_area14': {
        'spider': [(4, 21), (15, 29), (20, 27), (20, 11), (8, 9)],
        'goblin': [(15, 14), (19, 17), (14, 24), (15, 30), (20, 5)],
        'wolf': [(15, 19), (6, 9), (15, 12), (20, 25)]
    },
    # 'yggdrasil': ['orc', 'ent', 'poison_snake', 'spirit', 'bear', 'killer_fungus',  'golem'],
    # 'combat_zone': [],
    'ancient_forest_area1': {
        'spider': [(35, 9), (24, 14), (18, 7), (10, 28), (7, 10), (19, 25), (15, 35)],
        'goblin': [(37, 25), (28, 37), (5, 6), (32, 8), (3, 11), (17, 19)],
        'wolf': [(28, 11), (10, 30), (3, 29)]
    },
    'ancient_forest_area2': {
        'spider': [(31, 32), (7, 32), (7, 22), (22, 19), (28, 12), (20, 7), (12, 12), (6, 9)],
        'killer_fungus': [(2, 7), (18, 6), (21, 20), (29, 11), (4, 34), (16, 21)]
    },
    'ancient_forest_area3': {
        'ent': [(3, 30), (7, 35), (7, 27), (16, 30), (35, 6)],
        'poison_snake': [(9, 10), (27, 6), (29, 27), (17, 17)],
        'killer_fungus': [(14, 12), (22, 23), (32, 27), (29, 16), (12, 8)]
    },
    'ancient_forest_dungeon': {
        'poison_snake': [(117, 63), (131, 6), (117, 50), (103, 71), (95, 62), (87, 68), (81, 51), (105, 87), (95, 94), (92, 119), (92, 101), (92, 134), (102, 138), (112, 131), (131, 121), (128, 130), (134, 141), (73, 116), (57, 122), (23, 123)],
        'killer_fungus': [(38, 110), (21, 123), (10, 117), (46, 122), (72, 122), (72, 99), (95, 90), (109, 87), (105, 63), (80, 64), (134, 78), (94, 135), (51, 122)],
        'ent': [(72, 67), (82, 51), (37, 103), (42, 123), (12, 121), (37, 94), (37, 76), (31, 71), (27, 59), (83, 90), (116, 119)]
    },
    # 'ancient_forest_village': [],
    # 'vulcanic_zone_area1': ['spider', 'goblin'],
    # 'vulcanic_zone_area2': ['goblin', 'wolf'],
    # 'vulcanic_zone_area3': ['goblin', 'wolf', 'poison_snake'],
    # 'vulcanic_zone_elder_cave': ['goblin', 'wolf', 'orc', 'poison_snake'],
    # 'vulcanic_zone_village': [],
    # 'snowfields_area1': ['goblin', 'wolf'],
    # 'snowfields_area2': ['wolf', 'bear'],
    # 'snowfields_area3': ['wolf', 'orc'],
    # 'snowfields_elder_cave': ['wolf', 'orc', 'spirit', 'bear'],
    # 'snowfields_village': [],
    # 'chrono_mountains_area1': ['spider', 'goblin', 'wolf'],
    # 'chrono_mountains_area2': ['goblin', 'wolf', 'bear'],
    # 'chrono_mountains_area3': ['goblin', 'wolf', 'orc'],
    # 'chrono_mountains_elder_cave': ['goblin', 'wolf', 'orc', 'poison_snake'],
    # 'chrono_mountains_village': []
}

enemy_list = {
    'spider': {
        'lv': 1,
        'name': 'spider',
        'hp': 500,
        'power': 33,
        'resistance': 27,
        'agility': 8,
        'aim': 80,
        'class_type': 'enemy',
        'exp': 15,
        'drops': [],
        'skills': [skill_list['base_attack']]
    },
    'goblin': {
        'lv': 1,
        'name': 'goblin',
        'hp': 750,
        'power': 43,
        'resistance': 35,
        'agility': 4,
        'aim': 70,
        'class_type': 'enemy',
        'exp': 25,
        'drops': [],
        'skills': [
            skill_list['base_attack'],
            skill_list['fireball']
        ],
    },
    'wolf': {
        'lv': 1,
        'name': 'wolf',
        'hp': 900,
        'power': 65,
        'resistance': 40,
        'agility': 12,
        'aim': 80,
        'class_type': 'enemy',
        'exp': 35,
        'drops': [],
        'skills': [
            skill_list['base_attack'],
            skill_list['fireball']
        ],
    },
    'orc': {
        'lv': 2,
        'name': 'orc',
        'hp': 1100,
        'power': 69,
        'resistance': 59,
        'agility': 3,
        'aim': 80,
        'class_type': 'enemy',
        'exp': 50,
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
        'hp': 800,
        'power': 64,
        'resistance': 46,
        'agility': 20,
        'aim': 80,
        'class_type': 'enemy',
        'exp': 50,
        'drops': [],
        'skills': [
            skill_list['base_attack'],
            skill_list['eruption']
        ],
    },
    'ent': {
        'lv': 3,
        'name': 'ent',
        'hp': 1700,
        'power': 50,
        'resistance': 70,
        'agility': 10,
        'aim': 80,
        'class_type': 'enemy',
        'exp': 70,
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
        'hp': 1200,
        'power': 60,
        'resistance': 120,
        'agility': 17,
        'aim': 80,
        'class_type': 'enemy',
        'exp': 70,
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
        'hp': 1350,
        'power': 90,
        'resistance': 75,
        'agility': 1,
        'aim': 80,
        'class_type': 'enemy',
        'exp': 83,
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
        'hp': 1200,
        'power': 58,
        'resistance': 56,
        'agility': 10,
        'aim': 80,
        'class_type': 'enemy',
        'exp': 56,
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
        'hp': 3500,
        'power': 100,
        'resistance': 170,
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

boss_list = {
    'great_fairy': {
        'lv': 25,
        'name': 'great_fairy',
        'hp': 10000,
        'power': 140,
        'resistance': 160,
        'agility': 20,
        'aim': 98,
        'class_type': 'boss',
        'exp': 500,
        'drops': [],
        'skills': [skill_list['base_attack']]
    },
}

boss_spots = {
    'ancient_forest_dungeon': {
        'great_fairy': (42, 33)
    }
}


class EnemySpawnController:
    """
    Handle enemy monster spawning.
    """

    def spawn(self):
        """
        Main spawn controller runner.
        Checks if is possible to spawn a new monster in an area.
        The spawn is considered an character_event.
        When a new enemy spawns, the controller broadcasts the event
        to all connected clients.
        """
        # Handle common enemy spawning in each game area
        for area in enemies_spots:
            # Ignore spawning if area already reached max enemy count
            spawned_count = SpawnedEnemy.objects.filter(area_location=area, class_type='enemy').count()
            if spawned_count >= areas[area]['max_enemies']:
                continue

            # Get possible enemy kinds that appear in the iterated area
            possible_enemies = enemies_spots[area]

            # randomly select an possible enemy to spawn
            enemy_type = enemy_list[choice(list(possible_enemies))]

            # randomly select a spawn position that this enemy allow
            spot = choice(possible_enemies[enemy_type['name']])

            # Creates a new atabase record for spawned enemy
            enemy = SpawnedEnemy.objects.create(
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
                position_x = spot[0],
                position_y = spot[1]
            )
            enemy.save()

            # Broadcast enemy spawning
            payload = {
                'event_type': 'enemy_spawn',
                'enemy_id': enemy.id,
                'enemy_name': enemy.name,
                'position_x': enemy.position_x,
                'position_y': enemy.position_y,
                'area': area,
                'lv': enemy.lv,
                'max_hp': enemy.max_hp,
                'current_hp': enemy.current_hp,
                'classType': 'enemy'
            }
            # publish_message(payload)
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

        # Handle boss spawning in each boss spots
        for area in boss_spots:
            for possible_boss, spot in boss_spots[area].items():
                spawned_count = SpawnedEnemy.objects.filter(area_location=area, name=possible_boss).count()
                if spawned_count > 0:
                    continue

                x, y = spot
                enemy_type = boss_list[possible_boss]
                boss = SpawnedEnemy.objects.create(
                    lv=enemy_type['lv'],
                    name=enemy_type['name'],
                    max_hp=enemy_type['hp'],
                    current_hp=enemy_type['hp'],
                    power=enemy_type['power'],
                    resistance=enemy_type['resistance'],
                    agility=enemy_type['agility'],
                    aim=enemy_type['aim'],
                    exp=enemy_type['exp'],
                    class_type='boss',
                    drops=json.dumps(enemy_type['drops']).encode('utf-8'),
                    skills=json.dumps(enemy_type['skills']).encode('utf-8'),
                    area_location=area,
                    effects=b'[]',
                    position_x = x,
                    position_y = y
                )
                boss.save()

                # Broadcast enemy spawning
                payload = {
                    'event_type': 'enemy_spawn',
                    'enemy_id': boss.id,
                    'enemy_name': boss.name,
                    'position_x': boss.position_x,
                    'position_y': boss.position_y,
                    'area': area,
                    'lv': boss.lv,
                    'max_hp': boss.max_hp,
                    'current_hp': boss.current_hp,
                    'classType': 'boss'
                }
                # publish_message(payload)
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
