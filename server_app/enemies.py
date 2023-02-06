from base64 import b64encode
import uuid
import json
import requests
from django.conf import settings
from random import choice, random
from server_app.skills import skill_list
from server_app.map_areas import areas
from server_app.engine import target_position_is_valid
from server_app.models import Character
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


class Enemy:
    def __init__(self, data, area):
        self.id = str(uuid.uuid4())
        self.name = data['name']
        self.lv = data['lv']
        self.max_hp = data['hp']
        self.max_sp = 99999
        self.current_hp = data['hp']
        self.current_sp = 99999
        self.power = data['power']
        self.resistance = data['resistance']
        self.agility = data['agility']
        self.aim = data['aim']
        self.drops = data['drops']
        self.skills = data['skills']
        self.effects = []
        self.exp = data['exp']
        self.class_type = data['class_type']
        self.is_ko = False
        self.area = areas[area]
        self.position_x = self._get_possible_pixel(self.area['size_x'])
        self.position_y = self._get_possible_pixel(self.area['size_y'])

    def _get_possible_pixel(self, area_max):
        return choice([48*i for i in range(1, (area_max//48)+1)])

    def move(self):
        directions = ['up', 'down', 'left', 'right', 'none']
        move_to = choice(directions)

        current_x, current_y = self.position_x, self.position_y

        if move_to == 'up':
            self.position_y -= 48
        elif move_to == 'down':
            self.position_y += 48
        elif move_to == 'right':
            self.position_x += 48
        elif move_to == 'left':
            self.position_x -= 48
        else:
            return

        if not target_position_is_valid([self.position_x, self.position_y], self.area['name']):
            self.position_x = current_x
            self.position_y = current_y
            return

        # broadcast enemy movement
        payload = {
            'enemy_id': self.id,
            'position_x': self.position_x,
            'position_y': self.position_y
        }
        OnCharacterEvent.char_event(params={
            'event_type': 'enemy_movement',
            'data': payload
        })


class EnemyList:     
    def __init__(self):
        self.enemies_spawned = {a: [] for a in areas}
        self._r_conn = Redis(host=REDIS_HOST, port=int(REDIS_PORT))
        self._r_conn.set('ggj23', json.dumps(self.enemies_spawned).encode('utf-8'))

    def setEnemyList(self, enemies_spawned):
        self.enemies_spawned = {a: [Serializer.serialize(c) for c in b] for a, b in enemies_spawned.items()}
        es = json.dumps(self.enemies_spawned).encode('utf-8')
        self._r_conn.set('ggj23', es)
        
    def getEnemyList(self):
        es = self._r_conn.get('ggj23')
        if not es:
            return {}
        
        es = json.loads(es.decode('utf-8'))
        es = {a: [Serializer.deserialize(c) for c in b] for a, b in es.items()}
        self.enemies_spawned = es
        return self.enemies_spawned

    def manage_enemies(self):
        spawn_chance = .4
        max_enemies_in_area = 20
            
        enemies_spawned = {}
        for area in areas:
            characters_in_area = Character.objects.filter(is_logged=True, area_location=area).count()
            if not characters_in_area:
                enemies_spawned[area] = []
                continue

            enemies_spawned[area] = [e for e in self.getEnemyList()[area] if not e.is_ko]
            possible_enemies = enemies_spots[area]
            
            if  (len(possible_enemies) > 0) and \
                (len(enemies_spawned[area]) < max_enemies_in_area) and \
                (random() < spawn_chance):
                    enemy_type = enemy_list[choice(possible_enemies)]
                    enemy = Enemy(enemy_type, area)
                    enemies_spawned[area].append(enemy)
                    
                    # broadcast enemy spawn
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
                    print(f'published enemy spawn: {payload}')
        
enemies_spawned = EnemyList()
            