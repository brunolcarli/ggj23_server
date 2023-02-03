import uuid
from random import choice
from server_app.skills import skill_list
from server_app.map_areas import areas
from server_app.engine import target_position_is_valid


enemies = {
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
        'skills': {
            skill_list['base_attack']
        },
        'effects': []
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
        'skills': {
            skill_list['base_attack'],
            skill_list['fireball']
        },
        'effects': []
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
        'skills': {
            skill_list['base_attack'],
            skill_list['fireball']
        },
        'effects': []
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
        'skills': {
            skill_list['base_attack'],
            skill_list['ice_lance'],
            skill_list['air_cutter']
        },
        'effects': []
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
        'skills': {
            skill_list['base_attack'],
            skill_list['eruption']
        },
        'effects': []
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
        'skills': {
            skill_list['base_attack'],
            skill_list['wind_cutter'],
            skill_list['windstorm']
        },
        'effects': []
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
        'skills': {
            skill_list['base_attack'],
            skill_list['fireball'],
            skill_list['eruption'],
            skill_list['windstorm'],
            skill_list['air_cutter']
        },
        'effects': []
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
        'skills': {
            skill_list['base_attack'],
            skill_list['eruption'],
            skill_list['air_cutter']
        },
        'effects': []
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
        'skills': {
            skill_list['base_attack'],
            skill_list['windstorm'],
            skill_list['blind'],
            skill_list['enemy_down']
        },
        'effects': []
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
        'skills': {
            skill_list['base_attack'],
            skill_list['rock_throw'],
            skill_list['eruption']
        },
        'effects': []
    },
}


enemies_spots = {
    'citadel': [],
    'open_fields': [],
    'yggdrasil': [],
    'combat_zone': [],
    'ancient_forest_area1': [],
    'ancient_forest_area2': [],
    'ancient_forest_area3': [],
    'ancient_forest_elder_cave': [],
    'ancient_forest_village': [],
    'vulcanic_zone_area1': [],
    'vulcanic_zone_area2': [],
    'vulcanic_zone_area3': [],
    'vulcanic_zone_elder_cave': [],
    'vulcanic_zone_village': [],
    'snowfields_area1': [],
    'snowfields_area2': [],
    'snowfields_area3': [],
    'snowfields_elder_cave': [],
    'snowfields_village': [],
    'chrono_mountains_area1': [],
    'chrono_mountains_area2': [],
    'chrono_mountains_area3': [],
    'chrono_mountains_elder_cave': [],
    'chrono_mountains_village': []
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
        self.effects = data['effects']
        self.exp = data['exp']
        self.is_ko = True
        self.area = areas[area]
        self.position_x = self._get_possible_pixel(self.area['size_x'])
        self.position_y = self._get_possible_pixel(self.area['size_y'])

    def _get_possible_pixel(self, area_max):
        return choice([48*i for i in range(1, (area_max)+1)])

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

        # TODO broadcast enemy movement
